import datetime
import random

from python.color_utils import hls_to_rgb_normalized, random_hls

FLUSH_LARGE_NUMBER = 200


def flush_all_pixels(send_function):
	pixels = []
	for led in range(FLUSH_LARGE_NUMBER):
		pixels.append((0, 0, 0))

	send_function(pixels)
	print("flushed!")


def random_rgb():
	return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def print_fps(timestamp: datetime.datetime):
	duration = datetime.datetime.now() - timestamp
	print(f"fps: {1/duration.total_seconds()}")
	return datetime.datetime.now()


def random_color_rgb():
	rand_hls = random_hls()
	hue, light, sat = rand_hls
	return hls_to_rgb_normalized(hue, light, sat)