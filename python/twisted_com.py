from twisted.internet import protocol
from twisted.internet.protocol import ReconnectingClientFactory


class Client(protocol.Protocol):
	"""Once connected, send a message, then print the result."""

	def __init__(self, callback: callable, master_sender=False):
		self.master_sender = master_sender
		self._callback = callback

	def connectionMade(self):
		print("connected to", self.transport.getPeer().port)
		# string = f"hello from {self.transport.getPeer().port} - {self.master_sender}"
		# self.transport.write(string.encode('ascii'))

	def dataReceived(self, data):
		"""As soon as any data is received, write it back."""
		self._callback(data, self.transport.getPeer().port)

	def connectionLost(self, reason):
		print("connection lost")


class Factory(ReconnectingClientFactory):
	maxDelay = 2  # Maximum delay between connection attempts (in seconds)
	factor = 1.5  # Factor by which the delay increases after each attempt
	master_sender = None

	def __init__(self, data_callback: callable, master_sender=False):
		self.master_sender = master_sender
		self._data_callback = data_callback

	def buildProtocol(self, addr):
		self.resetDelay()
		return Client(callback=self._data_callback, master_sender=self.master_sender,)

	def clientConnectionLost(self, connector, reason):
		print('Lost connection.  Reason:', reason)
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		print('Connection failed. Reason:', reason)
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
