import datetime
import random

from python.config import leds_per_ring, RAIN_LIT_LEDS_PER_TREE


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
	rate = random.randrange(20, 40)
	now = datetime.datetime.now()
	return [get_led_color(), 0, True, rate, now]


def rain_init():

	leds = {}
	for _ in range(RAIN_LIT_LEDS_PER_TREE):
		led_on_tree = random.randrange(0, leds_per_ring)
		leds[led_on_tree] = rain_init_led()

	return {'leds': leds}


def rain_leds(data):
	pixels = [(0, 0, 0) for _ in range(leds_per_ring)]
	kill_list = []

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

	if kill_list:
		for kill_led in kill_list:
			del data['leds'][kill_led]
			led_on_tree = random.randrange(0, leds_per_ring)
			data['leds'][led_on_tree] = rain_init_led()
	return pixels
