import datetime
import random

from python.color_utils import hls_to_rgb_normalized, random_hls

FLUSH_LARGE_NUMBER = 300


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
	print(f"fps: {1 / duration.total_seconds()}")
	return datetime.datetime.now()


def random_color_rgb():
	rand_hls = random_hls()
	hue, light, sat = rand_hls
	return hls_to_rgb_normalized(hue, light, sat)


def translate(value, left_min, left_max, right_min, right_max):
	# Figure out how 'wide' each range is
	leftSpan = left_max - left_min
	rightSpan = right_max - right_min

	# Convert the left range into a 0-1 range (float)
	valueScaled = float(value - left_min) / float(leftSpan)

	# Convert the 0-1 range into a value in the right range.
	return right_min + (valueScaled * rightSpan)
