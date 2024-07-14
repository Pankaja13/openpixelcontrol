import argparse
import datetime
import random
import time

from twisted.internet import reactor, task

from python.config import trees_config, SHOW_FPS, TARGET_FPS, ENABLE_NETWORKING, AUDIO_PC_IP, mode_str_to_int, \
	leds_per_ring, chant_file_to_color, sound_file_envelops, PD_AMPLITUDE_LOW, PD_AMPLITUDE_HIGH, FLOAT_LOW, FLOAT_HIGH
from python.mode_manager import Modes, Tree
from python.modes.rain import new_lighting
from python.twisted_com import Factory
from python.utils import flush_all_pixels, random_color_rgb, translate

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


def buffer_messages(encoded_messages):
	decoded_data = str(encoded_messages.decode('ascii'))
	decoded_data = decoded_data.replace("\n", "").strip()
	split_data = decoded_data.split(';')[:-1]

	for message in split_data:
		if "sound" in message:
			return message

	return split_data[-1]


def get_mode_from_string(string):
	modes = mode_str_to_int[string]
	if type(modes) == list:
		return Modes(random.choice(modes))
	else:
		return Modes(modes)


def data_received(data, this_port):
	# print(f"{port} ==> {data}")
	message = buffer_messages(data)
	split_msg = message.split(" ")
	# message from tree
	if this_port in pd_ports:
		try:
			tree_obj: Tree = next((this_tree for this_tree in trees_data if this_tree.pd_port == port), None)
			# print(tree_obj.pd_port, '>>>>>>>>>>>>>>>>>')
			# print(split_msg)

			if split_msg[0] == 'sound':
				print('mode change!', split_msg)
				if len(split_msg) >= 3:
					length_of_sound_ms = int(float(split_msg[2]))
					mode_str, sound_file = split_msg[1].split('/')
					duration = datetime.timedelta(milliseconds=length_of_sound_ms)
					try:
						target_mode = get_mode_from_string(mode_str)
						if target_mode != tree_obj.mode:
							print('Changing mode to', target_mode)
							tree_obj.reinit(target_mode)

					except BaseException:
						print("Mode parse fail")

					if tree_obj.mode == Modes.SHIMMER:
						try:
							color = chant_file_to_color[sound_file]
							tree_obj.tree_data['color'] = color
						except BaseException:
							print('filename lookup error')

					if tree_obj.mode == Modes.RAIN:
						if sound_file == "thunder.wav":
							# activate lightening
							tree_obj.tree_data['mode_data']['should_trigger'] = True
							tree_obj.tree_data['mode_data']['lightning_pattern'] = new_lighting()

					if tree_obj.mode == Modes.CIRCLE_LOAD:
						try:
							load_dur, fade_dur = sound_file_envelops.get(sound_file)
						except BaseException:
							load_dur, fade_dur = length_of_sound_ms * 0.7, length_of_sound_ms * 0.3

						tree_obj.tree_data['circle_load_data']['is_filling'] = True
						tree_obj.tree_data['circle_load_data']['load_duration'] = datetime.timedelta(milliseconds=load_dur)
						tree_obj.tree_data['circle_load_data']['fade_duration'] = datetime.timedelta(milliseconds=fade_dur)
						tree_obj.tree_data['circle_load_data']['load_start_time'] = datetime.datetime.now()
						tree_obj.tree_data['circle_load_data']['offset'] = random.randint(0, leds_per_ring)
						tree_obj.tree_data['circle_load_data']['color'] = random_color_rgb()

					if tree_obj.mode == Modes.JUMP:
						try:
							load_dur, _ = sound_file_envelops.get(sound_file)
						except BaseException:
							load_dur = length_of_sound_ms * 0.7

						start_angle = random.randint(0, 360)
						end_angle = (start_angle + random.randint(90, 360)) % 360

						tree_obj.tree_data['data']['start_time'] = datetime.datetime.now()
						tree_obj.tree_data['data']['duration'] = datetime.timedelta(milliseconds=load_dur)
						tree_obj.tree_data['data']['start_angle'] = start_angle
						tree_obj.tree_data['data']['end_angle'] = end_angle
						tree_obj.tree_data['data']['color'] = random_color_rgb()
						tree_obj.tree_data['data']['reverse'] = random.choice([True, False])

					if tree_obj.mode == Modes.SEG_ROTATE:
						tree_obj.tree_data = tree_obj.get_new_init_data(duration_s=duration.seconds)

			elif len(split_msg) >= 2 and split_msg[0] == "amplitude":
				# Set Amplitude
				amplitude = int(float(split_msg[1]))
				if tree_obj.mode == Modes.RAIN:
					tree_obj.tree_data['mode_data']['rain_leds'] = amplitude * 2

				if tree_obj.mode == Modes.SHIMMER:
					translated_amplitude = translate(amplitude, 50, 80, 0.2, 0.9)

					average_window: list = tree_obj.tree_data['average_window'][1:]
					average_window.append(translated_amplitude)

					tree_obj.tree_data['amplitude'] = sum(average_window) / len(average_window)
					tree_obj.tree_data['average_window'] = average_window

				if tree_obj.mode == Modes.SEG_ROTATE:
					tree_obj.tree_data['data']['amplitude'] = translate(amplitude, 50, 80, 0.5, 1)

				if tree_obj.mode == Modes.LINE_TRANSPORT:
					tree_obj.tree_data['amplitude'] = translate(amplitude, PD_AMPLITUDE_LOW, PD_AMPLITUDE_HIGH, FLOAT_LOW, FLOAT_HIGH)

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
		mode_id = args.default_mode
		trees_data.append(Tree(Modes(mode_id), args.host, args.channel, args.pd_port))
		pd_ports.append(args.pd_port)

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
			print(port, "<<<<<<<")
			reactor.connectTCP(AUDIO_PC_IP, port, f)

	loop = task.LoopingCall(update_leds)
	loopDeferred = loop.start(1 / TARGET_FPS)
	loopDeferred.addErrback(loop_failed)

	try:
		reactor.run()
	finally:
		for tree in trees_data:
			flush_all_pixels(tree.send_data)
