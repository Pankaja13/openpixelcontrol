import math
import random
from datetime import datetime, timedelta

from python.color_utils import rotate
from python.config import leds_per_ring


def init():
	return {'circle_load_data': {
		"start_angle": 270,
		"leave_angle": 180,
		"color": (255, 100, 100),
		"number_of_leds": 10,
		"start_time": datetime.now(),
		"duration": timedelta(seconds=1),
		"reverse": False
	}}


def update(tree_data):
	data = tree_data['circle_load_data']

	if data["leave_angle"] < data["start_angle"]:
		data["leave_angle"], data["start_angle"] = data["start_angle"], data["leave_angle"]

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

	return pixels
