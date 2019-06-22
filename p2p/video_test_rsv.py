import pickle
import socket
import struct
import zlib
import numpy as np

import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)



HOST = '192.168.29.170'
PORT = 8082



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind(('192.168.29.170', 4000))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

client, addr = s.accept()
def recvall(size):
    databytes = b''
    while len(databytes) != size:
        to_read = size - len(databytes)
        if to_read > (2048):
            databytes += client.recv(2048)
        else:
            databytes += client.recv(to_read)
    return databytes


data = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED

while True:
    lengthbuf = recvall(4)
    length, = struct.unpack('!I', lengthbuf)
    databytes = recvall(length)
    img = zlib.decompress(databytes)
    if len(databytes) == length:
        print("Recieving Media..")
        print("Image Frame Size:- {}".format(len(img)))
        img = np.array(list(img))
        img = np.array(img, dtype = np.uint8).reshape(150, 200, 3)
        print(img)
        print(len(img), len(img[0]),len(img[0][0]))
        cv2.imshow("Stream", img)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
