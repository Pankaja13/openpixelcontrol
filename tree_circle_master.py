import time

from twisted.internet import reactor, task

from python.config import trees_config, PYTHON_CONTROL_PORT, PD_TREE_PORT_PREFIX
from python.mode_manager import Modes, Tree
from python.twisted_com import Factory
from python.utils import flush_all_pixels

trees_data = []

for this_tree_config in trees_config:
	mode_id = this_tree_config.get('default_mode') or 1
	trees_data.append(Tree(Modes(mode_id), this_tree_config['host'], this_tree_config['channel']))


def update_leds():
	list_start = time.time()
	for number, tree in enumerate(trees_data):
		start = time.time()
		# for each tree
		pixels = tree.get_pixels()
		if pixels:
			tree.send_data(pixels)

		try:
			current_fps = 1 / (time.time() - start)
			print(f"fps: {int(current_fps)}")
		except ZeroDivisionError:
			pass

	print(time.time() - list_start)
	time.sleep(0.001)


def data_received(data, port):
	print(f"{port} ==> {data}")
	decoded_data = data.decode('ascii')
	split_msg = decoded_data[:-1].split(' ')
	print(split_msg)

	if port == PYTHON_CONTROL_PORT:
		cmd_tree = int(split_msg[0])
		if split_msg[1] == "mode":
			new_mode = Modes(int(split_msg[2]))
			tree_obj: Tree = trees_data[cmd_tree - 1]
			tree_obj.reinit(new_mode)
			print(tree_obj.mode)
	else:
		# message from tree
		if PD_TREE_PORT_PREFIX < port < PD_TREE_PORT_PREFIX + 25:
			try:
				tree_no = port - 3000
				tree_obj: Tree = trees_data[tree_no - 1]

				if tree_obj.mode == Modes.RAIN:
					if len(split_msg) >= 2 and split_msg[0] == "amplitude":
						# set amplitude
						amplitude = int(split_msg[1])
						tree_obj.tree_data['mode_data']['rain_leds'] = amplitude

						if amplitude > 250:
							# activate lightening
							tree_obj.tree_data['mode_data']['should_trigger'] = True
							pass
			except IndexError:
				pass


def loop_failed(failure):
	"""
	Called when loop execution failed.
	"""
	print(failure.getBriefTraceback())
	reactor.stop()


f = Factory(data_received)
for x in range(1, 26):
	reactor.connectTCP("localhost", 3000 + x, f)
reactor.connectTCP("localhost", 4000, f)

fps = 120

loop = task.LoopingCall(update_leds)
loopDeferred = loop.start(1 / fps)
loopDeferred.addErrback(loop_failed)

try:
	reactor.run()
finally:
	for tree in trees_data:
		flush_all_pixels(tree.send_data)
