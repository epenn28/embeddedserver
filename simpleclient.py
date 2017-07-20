import socket
import sys
import binascii
import time

def sensorPacket(loopVal):
    header = "0F"
    source = "00"
    value = 0x04102011
    if (loopVal % 3 == 0):
        value = value + 0x100
    else:
        pass
    value = str(value)
    footer = "F0"
    dataToSend = header + source + value + footer
    message = binascii.unhexlify(dataToSend)
    return message

def encoderPacket():
    header = "0F"
    source = "01"
    value = "01020300"
    footer = "F0"
    dataToSend = header + source + value + footer
    message = binascii.unhexlify(dataToSend)
    return message

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('192.168.1.100', 2000)

    sock.connect(address)

    message = ""

    try:
        for i in range(256):
            if (i % 2 == 0):
                message = sensorPacket(i)
            else:
                message = encoderPacket()

            sock.send(message)
            time.sleep(0.02)

    finally:
        print("Closing socket")
        sock.close()

if __name__ == '__main__':
    main()
