import datetime
from enum import Enum

from python import opc
from python.config import leds_per_ring
from python.modes import twinkle, lightning, rain


def off_leds(_data):
	return [(0, 0, 0) for _ in range(leds_per_ring)]


class Modes(Enum):
	OFF = 1
	TWINKLE = 2
	LIGHTNING = 3
	RAIN = 4


class Tree:
	clients = {}

	init_functions = {
		Modes.OFF: lambda: None,
		Modes.TWINKLE: twinkle.twinkle_init,
		Modes.LIGHTNING: lightning.init,
		Modes.RAIN: rain.rain_init
	}

	led_functions = {
		Modes.OFF: off_leds,
		Modes.TWINKLE: twinkle.twinkle_leds,
		Modes.LIGHTNING: lightning.update,
		Modes.RAIN: rain.rain_leds
	}

	def __init__(self, mode: Modes, host, channel):
		self.tree_data = self.init_functions[mode]()
		self.mode = mode
		self.last_led_update = datetime.datetime.now()
		self.host = host
		self.channel = channel

		if host not in self.clients:
			client = opc.Client(host)

			if client.can_connect():
				print('connected to %s' % host)
			else:
				print('WARNING: could not connect to %s' % host)
			self.clients[host] = client

	def get_pixels(self):
		if datetime.datetime.now() - self.last_led_update < datetime.timedelta(milliseconds=50):
			return None
		self.last_led_update = datetime.datetime.now()
		return self.led_functions[self.mode](self.tree_data)

	def send_data(self, pixels):
		# print("channel", self.channel)
		return self.clients.get(self.host).put_pixels(pixels, channel=self.channel)
