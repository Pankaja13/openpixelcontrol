import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

socker_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socker_server.settimeout(None)
socker_server.bind((HOST, PORT))
socker_server.listen(1)
con, addr = socker_server.accept()


def check():
    global con, addr
    data = con.recv(1024)
    if data:
        print(data.decode())
        con.send("world".encode())
    if not data:
        con, addr = socker_server.accept()


while True:
    check()
