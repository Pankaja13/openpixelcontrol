import random
from datetime import datetime, timedelta

from python.color_utils import rotate, random_hls, hls_to_rgb_normalized
from python.config import leds_per_ring


def init():
	rand_hls = random_hls()
	hue, light, sat = rand_hls
	rgb_color = hls_to_rgb_normalized(hue, light, sat)
	return {'circle_load_data': {
		"is_filling": True,
		"color": rgb_color,
		"load_duration": timedelta(seconds=0.4),
		"fade_duration": timedelta(seconds=2),
		"load_start_time": datetime.now(),
		"fade_start_time": None,
		"offset": random.randint(0, leds_per_ring)
	}}


def update(tree_data):
	data = tree_data['circle_load_data']

	if data['is_filling'] is True:
		if (datetime.now() - data['load_start_time']) <= data['load_duration']:
			pixel_data = []
			to_fill = int(leds_per_ring * ((datetime.now() - data['load_start_time']) / data['load_duration']))

			for led_number in range(leds_per_ring):
				if led_number < to_fill:
					pixel_data.append(data['color'])
				else:
					pixel_data.append((0, 0, 0))
			pixel_data = rotate(pixel_data, data['offset'])
			return pixel_data

		else:
			data['is_filling'] = False
			data['fade_start_time'] = datetime.now()

	if data['is_filling'] is False:
		if (datetime.now() - data['fade_start_time']) >= data['fade_duration']:
			data['is_filling'] = None
		else:
			fade_mod = 1 - ((datetime.now() - data['fade_start_time']) / data['fade_duration'])
			color = (data["color"][0] * fade_mod, data["color"][1] * fade_mod, data["color"][2] * fade_mod)
			pixels = [color for _ in range(leds_per_ring)]
			return pixels

	if data['is_filling'] is None:
		return []
