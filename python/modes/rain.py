from datetime import datetime, timedelta
import random

from python.config import leds_per_ring, RAIN_INITIAL_LIT_LEDS_PER_TREE


def get_led_color():
	leds = [
		(39, 55, 89),
		(53, 138, 191),
		(41, 130, 165),
		(93, 173, 191),
		(159, 242, 234),
		(1, 24, 38),
		(35, 84, 114),
		(47, 114, 140),
		(131, 174, 191),
		(168, 202, 216),
	]
	return random.choice(leds)


def rain_init_led():
	# color, current brightness, isIncreasing?, rate, lastTime
	rate = round(random.triangular(7, 20, 15))

	now = datetime.now()
	return [get_led_color(), 0, True, rate, now]


def generate_lighting_pattern():
	envelops = []
	for _ in range(random.randint(1, 5)):
		envelops.append(timedelta(milliseconds=(random.randint(50, 200))))
		envelops.append(timedelta(milliseconds=(random.triangular(50, 600, 300))))
	return envelops


def new_lighting():
	lightning_pattern = generate_lighting_pattern()

	for index, envelop in enumerate(lightning_pattern):
		if index > 0:
			lightning_pattern[index] += lightning_pattern[index - 1]

	return lightning_pattern


def rain_init():
	leds = {}
	for _ in range(RAIN_INITIAL_LIT_LEDS_PER_TREE):
		led_on_tree = random.randrange(0, leds_per_ring)
		leds[led_on_tree] = rain_init_led()

	mode_data = {
		"is_on": False,
		"intensity": 250,
		"should_trigger": False,
		"lightning_start_time": None,
		"rain_leds": 300,
		"lightning_pattern": new_lighting(),
	}

	return {'leds': leds, 'mode_data': mode_data}


def rain_leds(data):
	pixels = [(0, 0, 0) for _ in range(leds_per_ring)]
	kill_list = []

	lightning_data = data['mode_data']

	# kill more leds
	kill_leds_faster = len(data['leds']) > lightning_data['rain_leds']

	def led_rebirth():
		missing = set(range(leds_per_ring)) - set(data['leds'].keys())
		random.choice(list(missing))
		led_on_tree = random.choice(list(missing))
		data['leds'][led_on_tree] = rain_init_led()

	if lightning_data['should_trigger'] and not lightning_data['is_on']:
		# brights on
		lightning_data['is_on'] = True
		lightning_data['should_trigger'] = False
		lightning_data['lightning_start_time'] = datetime.now()
		print('switch mode')

	elif lightning_data['is_on']:
		# time to change mode
		if len(lightning_data['lightning_pattern']) == 0 or datetime.now() - lightning_data['lightning_start_time'] > lightning_data['lightning_pattern'][0]:

			# brights off
			print('off')
			if lightning_data['lightning_pattern']:
				lightning_data['lightning_pattern'].pop(0)
			lightning_data['is_on'] = False

		else:
			# print('on')
			intensity = lightning_data['intensity']
			pixels = [(intensity, intensity, intensity) for _ in range(leds_per_ring)]
			return pixels

	elif not lightning_data['is_on'] and lightning_data['lightning_pattern'] and lightning_data['lightning_start_time']:
		if datetime.now() - lightning_data['lightning_start_time'] > lightning_data['lightning_pattern'][0]:
			# print('on again', lightning_data['lightning_pattern'])
			lightning_data['is_on'] = True
			if lightning_data['lightning_pattern']:
				lightning_data['lightning_pattern'].pop(0)
			print('on')

	if not lightning_data['is_on'] or len(lightning_data['lightning_pattern']) == 0:

		for led, led_data in data['leds'].items():
			brightness = led_data[1]
			isIncreasing = led_data[2]
			rate = led_data[3]

			if isIncreasing:
				brightness = brightness + rate
				if brightness > 250:
					data['leds'][led][2] = False
			else:
				if kill_leds_faster:
					rate = rate * 20
				brightness -= rate
				if brightness < 5:
					kill_list.append(led)
			data['leds'][led][1] = brightness

			pixels[led] = tuple(int(brightness * subpixel / 255) for subpixel in led_data[0])

		if kill_list:
			for kill_led in kill_list:
				del data['leds'][kill_led]

				# Let Die
				if not len(data['leds']) > lightning_data['rain_leds']:
					led_rebirth()

		# adding leds
		if len(data['leds']) < lightning_data['rain_leds']:
			missing_count = lightning_data['rain_leds'] - len(data['leds'])
			for _ in range(missing_count):
				led_rebirth()
		return pixels
