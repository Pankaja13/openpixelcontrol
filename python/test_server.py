import traceback

from twisted.internet import protocol, reactor
from twisted.internet.protocol import Factory


listeners = {}

CONTROL_IN_PORT = 2000


class Echo(protocol.Protocol):

	def __init__(self):
		self._port = None

	def connectionMade(self):
		self._port = self.transport.getHost().port
		print(self._port)
		listeners[self._port] = self

	@staticmethod
	def send_to_tree(tree_no, message):
		try:
			client = listeners[3000 + tree_no]
			client.transport.write(message.encode('ascii'))
		except KeyError:
			print(f"Client {tree_no} not connected")

	@staticmethod
	def broadcast(message: str):
		for listener in listeners:
			if listeners[listener].transport.getHost().port != CONTROL_IN_PORT:
				print(f"Control -> Listener ({listeners[listener].transport.getHost().port})", message)
				listeners[listener].transport.write(message.encode('ascii'))

	def dataReceived(self, data):
		port = self.transport.getHost().port
		if port != CONTROL_IN_PORT:
			return
		print(data, port)
		decoded_data = data.decode('ascii')
		try:
			if decoded_data[-1] != ';':
				print('bad format')
				return
			split_data: list = decoded_data[:-1].split(' ')
			if split_data[0] == "tree":
				tree_no = int(split_data[1])
				print(f'send data to tree number {tree_no}')
				print(' '.join(split_data[2:]))
				self.send_to_tree(tree_no, "")
		except BaseException as e:
			traceback.print_exc()
			print(e)
			return

	def connectionLost(self, reason):
		if self._port in listeners:
			del listeners[self._port]


class EchoFactory(Factory):

	def buildProtocol(self, addr):
		return Echo()


if __name__ == '__main__':
	for x in range(1, 26):
		reactor.listenTCP(3000 + x, EchoFactory())
	reactor.listenTCP(4000, EchoFactory())
	reactor.listenTCP(2000, EchoFactory())
	reactor.run()
