#! python3
from python import opc

# everything is a nail
NUMBER_OF_PIXELS = 10000

IP_PORT = '127.0.0.1:7890'


client = opc.Client(IP_PORT)

if client.can_connect():
    print('connected to %s' % IP_PORT)
else:
    print('WARNING: could not connect to %s' % IP_PORT)


pixels = []
# only first branch, first tree
for led in range(NUMBER_OF_PIXELS):
    pixels.append((0, 0, 0))
client.put_pixels(pixels, channel=0)

print(f"{NUMBER_OF_PIXELS} pixels flushed!")





