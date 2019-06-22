import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import zlib

cap=cv2.VideoCapture(0)
cap.set(3, 200)
cap.set(4, 150)
lnF = 200*150*3


# # Connecting to Champaign
# HOST = '96.63.228.98'
# PORT = 4500
#
# HOST = '104.244.64.123'
# PORT = 4000
# client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# client.connect(('192.168.29.123', 4000))
# MSG_BUF_SIZE = 2048

while True:

    # Serialize frame
    ret, frame = cap.read()
    cv2.imshow("Send", frame)
    key = cv2.waitKey(1)
    if key in [27, 81, 113]:
        break
    # cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # frame = cv2.resize(frame, (200, 150))
    # frame = np.array(frame, dtype = np.uint8).reshape(1, lnF)
    # jpg_as_text = bytearray(frame)
    #
    # databytes = zlib.compress(jpg_as_text, 9)
    # length = struct.pack('!I', len(databytes))
    # bytesToBeSend = b''
    # client.sendall(length)
    # while len(databytes) > 0:
    #     if (MSG_BUF_SIZE) <= len(databytes):
    #         bytesToBeSend = databytes[:(MSG_BUF_SIZE)]
    #         databytes = databytes[(MSG_BUF_SIZE):]
    #         client.sendall(bytesToBeSend)
    #     else:
    #         bytesToBeSend = databytes
    #         client.sendall(bytesToBeSend)
    #         databytes = b''
    # print("##### Data Sent!! #####")
