from datetime import datetime, timedelta

from python.config import leds_per_ring


def init():

	return {'lightning_data': {
		"is_on": False,
		"intensity": 250,
		"should_trigger": True,
		"trigger_time": None,
		"on_duration_ms": 100
	}}


def update(tree_data):
	lightning_data = tree_data['lightning_data']

	if lightning_data['should_trigger'] and not lightning_data['is_on']:
		intensity = lightning_data['intensity']
		pixels = [(intensity, intensity, intensity) for _ in range(leds_per_ring)]
		lightning_data['is_on'] = True
		lightning_data['should_trigger'] = False
		lightning_data['trigger_time'] = datetime.now()
		return pixels

	if lightning_data['is_on'] and lightning_data['trigger_time'] and datetime.now() - lightning_data['trigger_time'] > timedelta(milliseconds=lightning_data['on_duration_ms']):
		pixels = [(0, 0, 0) for _ in range(leds_per_ring)]
		lightning_data['is_on'] = False
		return pixels



