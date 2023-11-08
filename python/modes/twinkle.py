import random
from enum import Enum

from python.color_utils import transition, hls_to_rgb_normalized, rotate
from python.config import leds_per_ring
from python.utils import random_rgb


class States(Enum):
	COLLECTING = 1
	FADE_TO_WHITE = 2
	WHITE_TO_RAINBOW = 3
	RAINBOW_TO_WHITE = 4
	RAINBOW_TO_BLACK = 5


def twinkle_init_led():
	return [random_rgb(), 0]


def twinkle_init():
	# leds = {}
	# for _ in range(TWINKLE_LEDS_PER_TREE):
	# 	led_on_tree = random.randrange(0, leds_per_ring)
	# 	leds[led_on_tree] = twinkle_init_led()

	rainbow = [hls_to_rgb_normalized(1/leds_per_ring*x, 0.5, 1) for x in range(300)]

	return {
		'leds': {},
		'mode_data': {
			'mode': States.COLLECTING,
			'fade_to_white_val': 0.0,
			'white_to_rainbow_val': 0.0,
			'rainbow_to_white_val': 0.0,
			'rainbow_to_black_val': 0.0,
			'loop_count': 0,
			'rainbow': rainbow
		}
	}


def twinkle_leds(data):
	pixels = []
	max_bright_count = 0

	if data['mode_data']['mode'] == States.COLLECTING:
		pixels = [(0, 0, 0) for _ in range(leds_per_ring)]

		if len(data['leds']) < leds_per_ring:
			for _ in range(round(random.triangular(0, 3, 2))):
				led_on_tree = random.randrange(0, leds_per_ring)
				data['leds'][led_on_tree] = twinkle_init_led()

		for led, led_data in data['leds'].items():
			brightness = led_data[1] + random.triangular(0, 5, 0.5)
			data['leds'][led][1] = brightness
			if brightness >= 254:
				max_bright_count += 1
			pixels[led] = tuple(int(brightness * subpixel / 255) for subpixel in led_data[0])

		if max_bright_count >= leds_per_ring:
			data['mode_data']['mode'] = States.FADE_TO_WHITE
			data['mode_data']['fade_to_white_val'] = 0.0

	elif data['mode_data']['mode'] == States.FADE_TO_WHITE:
		if data['mode_data']['fade_to_white_val'] <= 2:
			for led, led_data in data['leds'].items():
				pixels.append(transition(led_data[0], (255, 255, 255), data['mode_data']['fade_to_white_val']))
				data['mode_data']['fade_to_white_val'] += 0.0001
		else:
			data['mode_data']['mode'] = States.WHITE_TO_RAINBOW
			data['mode_data']['white_to_rainbow_val'] = 0
			data['mode_data']['loop_count'] += 1
			print(data['mode_data']['loop_count'])

	elif data['mode_data']['mode'] == States.WHITE_TO_RAINBOW:
		if data['mode_data']['white_to_rainbow_val'] < 2.0:
			data['mode_data']['rainbow'] = rotate(data['mode_data']['rainbow'], round(random.triangular(0, 0.7, 0.3)))
			data['mode_data']['white_to_rainbow_val'] += 0.01
			pixels = [transition((255, 255, 255), color, data['mode_data']['white_to_rainbow_val']) for color in data['mode_data']['rainbow']]
		else:
			data['mode_data']['mode'] = States.RAINBOW_TO_WHITE
			data['mode_data']['rainbow_to_white_val'] = 0

	elif data['mode_data']['mode'] == States.RAINBOW_TO_WHITE:
		# print(data['mode_data']['rainbow_to_white_val'])
		if data['mode_data']['rainbow_to_white_val'] < 0.9:
			data['mode_data']['rainbow'] = rotate(data['mode_data']['rainbow'], round(random.triangular(0, 0.7, 0.3)))
			data['mode_data']['rainbow_to_white_val'] += 0.03
			pixels = [transition(color, (255, 255, 255), data['mode_data']['rainbow_to_white_val']) for color in data['mode_data']['rainbow']]
		else:
			data['mode_data']['mode'] = States.WHITE_TO_RAINBOW
			data['mode_data']['white_to_rainbow_val'] = 0
			data['mode_data']['loop_count'] += 1
			if data['mode_data']['loop_count'] > 5:
				data['mode_data']['mode'] = States.RAINBOW_TO_BLACK
				data['mode_data']['loop_count'] = 0
				data['mode_data']['rainbow_to_black_val'] = 0

	elif data['mode_data']['mode'] == States.RAINBOW_TO_BLACK:
		if data['mode_data']['rainbow_to_black_val'] < 2:
			data['mode_data']['rainbow'] = rotate(data['mode_data']['rainbow'], round(random.triangular(0, 0.7, 0.3)))
			data['mode_data']['rainbow_to_black_val'] += 0.01
			pixels = [transition(color, (0, 0, 0), data['mode_data']['rainbow_to_black_val']) for color in data['mode_data']['rainbow']]
		else:
			data['mode_data']['mode'] = States.COLLECTING
			data['leds'] = {}
	# if len(pixels) > 1:
	# 	print(pixels[0])

	# if kill_list:
	# 	for kill_led in kill_list:
	# 		del data['leds'][kill_led]
	# 		led_on_tree = random.randrange(0, leds_per_ring)
	# 		data['leds'][led_on_tree] = twinkle_init_led()
	return pixels
