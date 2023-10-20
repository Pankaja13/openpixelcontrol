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
	rate = random.randrange(1, 8)
	now = datetime.now()
	return [get_led_color(), 0, True, rate, now]


def rain_init():

	leds = {}
	for _ in range(RAIN_INITIAL_LIT_LEDS_PER_TREE):
		led_on_tree = random.randrange(0, leds_per_ring)
		leds[led_on_tree] = rain_init_led()

	mode_data = {
		"is_on": False,
		"intensity": 250,
		"should_trigger": True,
		"trigger_time": None,
		"on_duration_ms": 1000,
		"rain_leds": 300
	}

	return {'leds': leds, 'mode_data': mode_data}


def rain_leds(data):
	pixels = [(0, 0, 0) for _ in range(leds_per_ring)]
	kill_list = []

	lightning_data = data['mode_data']

	if lightning_data['should_trigger'] and not lightning_data['is_on']:
		intensity = lightning_data['intensity']
		pixels = [(intensity, intensity, intensity) for _ in range(leds_per_ring)]
		lightning_data['is_on'] = True
		lightning_data['should_trigger'] = False
		lightning_data['trigger_time'] = datetime.now()
		return pixels

	if lightning_data['is_on'] and lightning_data['trigger_time'] and datetime.now() - lightning_data['trigger_time'] > timedelta(milliseconds=lightning_data['on_duration_ms']):
		pixels = [get_led_color() for _ in range(leds_per_ring)]
		lightning_data['is_on'] = False
		return pixels
	else:
		if lightning_data['is_on']:
			return []

		for led, led_data in data['leds'].items():
			brightness = led_data[1]
			isIncreasing = led_data[2]
			rate = led_data[3]

			if isIncreasing:
				brightness = brightness + rate
				if brightness > 250:
					data['leds'][led][2] = False
			else:
				brightness -= rate
				if brightness < 5:
					kill_list.append(led)
			data['leds'][led][1] = brightness

			pixels[led] = tuple(int(brightness * subpixel / 255) for subpixel in led_data[0])

	def led_rebirth():
		missing = set(range(leds_per_ring)) - set(data['leds'].keys())
		random.choice(list(missing))
		led_on_tree = random.choice(list(missing))
		data['leds'][led_on_tree] = rain_init_led()

	if kill_list:
		for kill_led in kill_list:
			del data['leds'][kill_led]

			# Let Die
			if len(data['leds']) > lightning_data['rain_leds']:
				print("too many")
				return

			led_rebirth()

	if len(data['leds']) < lightning_data['rain_leds']:
		missing_count = lightning_data['rain_leds'] - len(data['leds'])
		for _ in range(missing_count):
			led_rebirth()

	print(len(data['leds']))

	return pixels
