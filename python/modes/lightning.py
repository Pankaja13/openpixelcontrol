import datetime
import random

from python.config import leds_per_ring, TWINKLE_LEDS_PER_TREE
from python.utils import random_rgb


def init():

	return {'lightning_data': {
		"is_on": False,
		"intensity": 250,
		"should_trigger": True,
		"trigger_time": None,
		"on_duration_ms": 100
	}}


def update(tree_data):
	data = tree_data['lightning_data']
	if data['should_trigger'] and not data['is_on']:
		intensity = data['intensity']
		pixels = [(intensity, intensity, intensity) for _ in range(leds_per_ring)]
		data['is_on'] = True
		data['should_trigger'] = False
		data['trigger_time'] = datetime.datetime.now()
		return pixels

	if data['trigger_time'] and datetime.datetime.now() - data['trigger_time'] > datetime.timedelta(milliseconds=data['on_duration_ms']):
		pixels = [(0, 0, 0) for _ in range(leds_per_ring)]
		return pixels



