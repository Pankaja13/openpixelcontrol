import datetime
import random
import time

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
