import argparse
import datetime
import gc
import time

from twisted.internet import reactor, task

from python.config import trees_config, PYTHON_CONTROL_PORT, PD_TREE_PORT_PREFIX, SHOW_FPS, SHOW_LAST_UPDATE, \
	TARGET_FPS, ENABLE_NETWORKING
from python.mode_manager import Modes, Tree
from python.twisted_com import Factory
from python.utils import flush_all_pixels

trees_data = []
pd_ports = []
last_update = time.time()


def update_leds():
	list_start = time.time()
	global last_update
	interval = time.time() - last_update
	# print('last Update', ' ' * (40 if interval > 1 else 0), time.time() - last_update, 1/interval)
	last_update = time.time()
	for number, tree in enumerate(trees_data):
		start = time.time()
		# for each tree
		pixels = tree.get_pixels()
		if pixels:
			tree.send_data(pixels)

		try:
			current_fps = 1 / (time.time() - start)
			if SHOW_FPS:
				print(f"fps: {int(current_fps)}")
		except ZeroDivisionError:
			pass
	if SHOW_FPS:
		print(time.time() - list_start)
	# time.sleep(0.001)


def data_received(data, port):
	print(f"{port} ==> {data}")
	decoded_data = str(data.decode('ascii'))
	decoded_data = decoded_data.strip("\n")
	if decoded_data.count(";") > 1:
		return
	split_msg = decoded_data[:-1].split(' ')

	if port == PYTHON_CONTROL_PORT:
		cmd_tree = int(split_msg[0])
		if split_msg[1] == "mode":
			new_mode = Modes(int(split_msg[2]))
			tree_obj: Tree = trees_data[cmd_tree - 1]
			tree_obj.reinit(new_mode)
			print(tree_obj.mode)
	else:
		# message from tree
		if port in pd_ports:
			try:
				tree_obj: Tree = next((this_tree for this_tree in trees_data if this_tree.pd_port == port), None)
				print(tree_obj, '>>>>>>>>>>>>>>>>>')
				if tree_obj.mode == Modes.RAIN:
					if len(split_msg) >= 2 and split_msg[0] == "amplitude":
						# set amplitude
						amplitude = int(split_msg[1])
						tree_obj.tree_data['mode_data']['rain_leds'] = amplitude

						if amplitude > 250:
							# activate lightening
							tree_obj.tree_data['mode_data']['should_trigger'] = True
				if tree_obj.mode == Modes.SHIMMER:
					if len(split_msg) >= 2 and split_msg[0] == "amplitude":
						# set amplitude
						amplitude = split_msg[1]
						tree_obj.tree_data['amplitude'] = (float(amplitude) - 40)/80

			except IndexError:
				pass


def loop_failed(failure):
	"""
	Called when loop execution failed.
	"""
	print(failure.getBriefTraceback())
	reactor.stop()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--host', '-H', type=str,)
	parser.add_argument('-pd_port', '-p', type=int)
	parser.add_argument('-c', '--channel', type=int, default=0)
	parser.add_argument('-m', '--default_mode', type=int, default=4)

	args = parser.parse_args()

	if args.host and args.pd_port:
		print(args)
		mode_id = args.default_mode
		trees_data.append(Tree(Modes(mode_id), args.host, args.channel, args.pd_port))
	else:
		# add trees from config
		for this_tree_config in trees_config:
			mode_id = this_tree_config.get('default_mode') or 1
			pd_port = this_tree_config['pd_port']
			pd_ports.append(pd_port)
			trees_data.append(Tree(Modes(mode_id), this_tree_config['host'], this_tree_config['channel'], pd_port))

	for tree in trees_data:
		print(tree.host, tree.pd_port, tree.mode, tree.channel)

	f = Factory(data_received)

	if ENABLE_NETWORKING:
		for port in pd_ports:
			reactor.connectTCP("localhost", port, f)
		reactor.connectTCP("localhost", PYTHON_CONTROL_PORT, f)

	loop = task.LoopingCall(update_leds)
	loopDeferred = loop.start(1 / TARGET_FPS)
	loopDeferred.addErrback(loop_failed)

	try:
		reactor.run()
	finally:
		for tree in trees_data:
			flush_all_pixels(tree.send_data)
