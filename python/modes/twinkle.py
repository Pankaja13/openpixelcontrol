import datetime
import random

from python.config import leds_per_ring, TWINKLE_LEDS_PER_TREE
from python.utils import random_rgb


def twinkle_init_led():
	# color, current brightness, isIncreasing?, rate, lastTime
	rate = random.randrange(5, 20)
	now = datetime.datetime.now()
	return [random_rgb(), 0, True, rate, now]


def twinkle_init():

	leds = {}
	for _ in range(TWINKLE_LEDS_PER_TREE):
		led_on_tree = random.randrange(0, leds_per_ring)
		leds[led_on_tree] = twinkle_init_led()

	return {'leds': leds}


def twinkle_leds(data):
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
			data['leds'][led_on_tree] = twinkle_init_led()
	return pixels
