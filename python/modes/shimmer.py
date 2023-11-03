import random
from datetime import datetime, timedelta

from python.color_utils import rotate
from python.config import leds_per_ring


def init():
	return {
		'shimmer_base': create_shimmer_base(),
		'shimmer_last_rotate': datetime.now(),
		'color': (125, 250, 34),
		'amplitude': 1.0,
		'average_window': [0] * 10
	}


def update(data):
	if datetime.now() - data['shimmer_last_rotate'] > timedelta(milliseconds=100):
		data['shimmer_base'] = rotate(data['shimmer_base'], 1)
		data['shimmer_last_rotate'] = datetime.now()

	pixels = []
	amplitude = data['amplitude']

	for gamma_data in data['shimmer_base']:
		gamma = gamma_data / 255
		color = data['color']
		led_color = round(color[0] * gamma * amplitude), round(color[1] * gamma * amplitude), round(color[2] * gamma * amplitude),

		pixels.append(led_color)

	return pixels


def create_shimmer_base():

	START_VALUE = 175

	pixels = []
	last_val_target = START_VALUE

	def get_next_point(pos):
		DIST_MAX = 20
		dist = random.randint(10, DIST_MAX)
		val = (random.randint(0, 100) - 50)

		if pos + DIST_MAX > leds_per_ring:
			dist = leds_per_ring - pos
			val = START_VALUE - last_val_target

		if 255 < (val + last_val_target) or (val + last_val_target) < 0:
			val = val * -1

		return {
			'end': pos + dist,
			'val': val,
			'start': pos
		}

	next_point = {
		'end': 0,
		'val': 0,
		'start': 0
	}

	for led_pos in range(leds_per_ring):
		if next_point['end'] < led_pos:
			last_val_target = next_point['val'] + last_val_target
			next_point = get_next_point(led_pos)

		progress = (led_pos - next_point['start']) / ((next_point['end'] - next_point['start']) or 1)

		led_val = last_val_target + (next_point['val'] * progress)
		pixels.append(round(led_val))

	pixels = rotate(pixels, random.randint(0, 200))

	return pixels


if __name__ == "__main__":
	print(create_shimmer_base())
