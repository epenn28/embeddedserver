import socket
import sys
import binascii
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('192.168.1.100', 2000)

sock.connect(address)

try:
    header = "0F"
    source = "00"
    value = "00"
    footer = "F0"
    for i in range(256):
        dataToSend = header + "{:02X}".format(i) + source + value + footer
        message = binascii.unhexlify(dataToSend)
        sock.send(message)
        time.sleep(0.02)

finally:
    print("Closing socket")
    sock.close()
