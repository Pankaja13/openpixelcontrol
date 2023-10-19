import sys

from twisted.internet import reactor, protocol


class Client(protocol.Protocol):
	"""Once connected, send a message, then print the result."""

	def __init__(self, master_sender=False):
		self.master_sender = master_sender

	def connectionMade(self):
		arg = sys.argv[1] if len(sys.argv) > 1 else "hi"
		data = arg.encode('ascii')
		self.transport.write(arg.encode('ascii'))
		print(f"sent => {data}")
		self.transport.loseConnection()


class Factory(protocol.ClientFactory):
	master_sender = None

	def __init__(self, master_sender=False):
		self.master_sender = master_sender

	def clientConnectionFailed(self, connector, reason):
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		reactor.stop()

	def buildProtocol(self, addr):
		return Client(self.master_sender)


if __name__ == '__main__':
	f = Factory()
	reactor.connectTCP("localhost", 2000, f)
	reactor.run()
