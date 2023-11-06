import math
import random
from datetime import datetime, timedelta

from python.config import leds_per_ring
from python.utils import random_color_rgb


def init(data=None):
	if data is None:
		data = {}
	duration_s = data.get('duration_s') or 10
	leave = random.randint(200, 360) * math.ceil(duration_s * random.randint(2, 5))
	return {'data': {
		"start_angle": random.randint(0, 360),
		"leave_angle": leave,
		"color": random_color_rgb(),
		"number_of_leds": random.randint(20, 200),
		"start_time": datetime.now(),
		"duration": timedelta(seconds=duration_s),
		"reverse": random.choice([True, False])
	}}


def update(tree_data):
	data = tree_data['data']

	pixels = [(0, 0, 0) for _ in range(leds_per_ring)]
	if (datetime.now() - data['start_time']) <= data['duration']:
		led_offset = int((data['start_angle'])/360 * leds_per_ring)
		progress = ((datetime.now() - data['start_time']) / data['duration'])
		total_arc_leds = math.ceil((data['leave_angle'] - data['start_angle'])/360 * leds_per_ring) + data["number_of_leds"]
		led_start_location = math.ceil(total_arc_leds * progress)
		led_end_location = max(led_start_location - data["number_of_leds"], 0)

		for led_number in range(led_end_location, led_start_location):
			if 0 <= led_number <= (total_arc_leds - data["number_of_leds"]):
				led_pos = (led_number + led_offset) % leds_per_ring
				pixels[led_pos] = data["color"]

	if data['reverse']:
		pixels.reverse()

	return pixels
