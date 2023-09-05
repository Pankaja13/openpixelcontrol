# echo-client.py

import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def send_message(message: str):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		s.sendall(message.encode())
		data = s.recv(1024)
		print(data)
		# time.sleep(10000)


send_message("hi")
