import sys

from twisted.internet import reactor, protocol


class Client(protocol.Protocol):
	"""Once connected, send a message, then print the result."""

	def __init__(self, master_sender=False):
		self.master_sender = master_sender

	def connectionMade(self):
		arg = sys.argv[1] if len(sys.argv) > 1 else "hi"
		self.transport.write(arg.encode('ascii'))
		self.transport.loseConnection()

	def dataReceived(self, data):
		print("data recieved from server:", data)

	def connectionLost(self, reason):
		print("connection lost")


class Factory(protocol.ClientFactory):
	master_sender = None

	def __init__(self, master_sender=False):
		self.master_sender = master_sender

	def clientConnectionFailed(self, connector, reason):
		print("Connection failed - goodbye!")
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print("Connection lost - goodbye!")
		reactor.stop()

	def buildProtocol(self, addr):
		return Client(self.master_sender)


if __name__ == '__main__':
	f = Factory()
	reactor.connectTCP("localhost", 2000, f)

	reactor.run()