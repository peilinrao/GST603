


"""
This is a p2p chat program.
Jun 16, 2019
Author: Jiyu Hu

Adding video feature by Peilin Rao
Attempt failed. Bad lagging happens. Continue a new version in p2pVideo2
"""
import cv2
import threading
import socket
import select
import sys
import os
import zmq
import base64
import numpy as np
import pickle
import struct
import zlib

#signals used for cummunication between nodes
RECONNECT = "\0\0\0"
DONE = "\n\n\n"
VIDEOMODEINIT = "\s\s\s"
VIDEOMODEACCEPT = "\e\e\e"

#constants
MSG_BUF_SIZE = 2048
PKG_SIZE = 4*2048
SIG_LENGTH = 128
STRFORMATSIZE = 37
BINFORMATSIZE = 33
payload_size = struct.calcsize("L")
lnf = FRAME_WIDTH*FRAME_HEIGHT*3



"""
class node:
    the basic unit of a p2p program. this class handles connection
    and commmunication between different nodes (computers).
    All computers running this piece of code will form a connected graph and
    messages are broadcasted throughout the network. When one of the nodes goes
    offline, it will tell all of its neighbors except one to reconnect to that
    one neighbor, thus maintaining connection between nodes.
"""
class node:
    # socket object that records the original connection. NULL of this node is
    # the first node in the network

    parent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket object that receives incoming connection requests
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # dictionary that stores the neighbor socket objects, there IP address and
    # port number
    neighbor = {}


    """
    recvNode(self):
        DESCRIPTION: a thread function that keeps polling for incoming
                     connection requests
        INPUT: self: node instance
        OUTPUT: NONE
        SIDEEFFECTS: accept connection from other sockets
    """
    def recvNode(self):
        while True:
            conn, addr = self.server.accept()
            print(">> " + addr[0] + " connected")
            temp = []
            temp.append(addr[0])
            temp.append(conn.recv(MSG_BUF_SIZE).decode())
            self.neighbor[conn] = temp

    def recvall(self, size, client):
        databytes = b''
        while len(databytes) != size:
            to_read = size - len(databytes)
            if to_read > (2048):
                databytes += client.recv(2048)
            else:
                databytes += client.recv(to_read)
        return databytes

    def rescale_frame(self,frame, percent=75):
        width = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def video_send(self, node):
        cap = cv2.VideoCapture(0)
        cap.set(3, FRAME_WIDTH)
        cap.set(4, FRAME_HEIGHT)
        while True:
            # Serialize frame
            ret, frame = cap.read()
            key = cv2.waitKey(1)
            cv2.imshow('sending',frame)
            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            frame = np.array(frame, dtype = np.uint8).reshape(1, FRAME_WIDTH*FRAME_HEIGHT*3)
            jpg_as_text = bytearray(frame)

            databytes = zlib.compress(jpg_as_text, 9)
            length = struct.pack('!I', len(databytes))
            bytesToBeSend = b''
            node.sendall(length)
            while len(databytes) > 0:
                if (MSG_BUF_SIZE) <= len(databytes):
                    bytesToBeSend = databytes[:(MSG_BUF_SIZE)]
                    databytes = databytes[(MSG_BUF_SIZE):]
                    node.sendall(bytesToBeSend)
                else:
                    bytesToBeSend = databytes
                    node.sendall(bytesToBeSend)
                    databytes = b''

    def video_receive(self, socks):
        while True:
            lengthbuf = self.recvall(4, socks)
            length, = struct.unpack('!I', lengthbuf)
            databytes = self.recvall(length, socks)
            img = zlib.decompress(databytes)
            if len(databytes) == length:
                print("Recieving Media..")
                print("Image Frame Size:- {}".format(len(img)))
                img = np.array(list(img))
                img = np.array(img, dtype = np.uint8).reshape(FRAME_HEIGHT, FRAME_WIDTH, 3)
                self.frame = img
                cv2.imshow('frame', self.frame)
                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()

    def video_render(self):
        while True:
            if self.render == 1:
                # frame150 = self.rescale_frame(self.frame, percent=400)
                # Display
                cv2.imshow('frame', self.frame)
                self.render = 0



    """
    nodeThread(self):
        DESCRIPTION: a thread function that keeps examining incoming messages
                     from other sockets
        INPUT: self: node instance
        OUTPUT: NONE
        SIDEEFFECTS: receive and send messages from and to other sockets
    """
    def nodeThread(self):
        while True:
            sockets_list = list(self.neighbor.keys())
            sockets_list.append(sys.stdin)
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [], 1)


            for socks in read_sockets:
                ##########################
                # receive others' message
                ##########################
                if socks != sys.stdin:
                    # NONE-VIDEOMOD
                    if self.VIDEORSV == 0:
                        message = socks.recv(MSG_BUF_SIZE).decode()

                        if message:
                            if message == RECONNECT:
                                print(self.neighbor[socks][0] + " disconnected.")
                                socks.send(DONE.encode())
                                message = socks.recv(MSG_BUF_SIZE).decode()
                                temp = message.split()
                                socks.close()
                                del self.neighbor[socks]
                                newSocks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                newSocks.connect((temp[0], int(temp[1])))
                                self.neighbor[newSocks] = temp
                                newSocks.send(str(self.Port).encode())

                            elif message == VIDEOMODEINIT:
                                print(socks,"wants to video chat with you! Accept?(y/n)")
                                answer = sys.stdin.readline()[:-1]
                                if answer == 'y':
                                    socks.send(VIDEOMODEACCEPT.encode())
                                # Waiting for socks to send video data
                                # ignore other received messages:
                                self.VIDEORSV = 1
                                self.video_receive(socks)
                            elif message == VIDEOMODEACCEPT:
                                #request has been accepted, send video data
                                print(socks,"accepted your request! Cyber Chat initialized...")
                                self.VIDEORSV = 0

                                self.video_send(socks)
                            else:
                                print('<' + self.neighbor[socks][0] + '> ' + message)
                                for node in self.neighbor.keys():
                                    if node != socks:
                                        node.send(message.encode())

                        else:
                            print(self.neighbor[socks][0] + " disconnected.")
                            socks.close()
                            del self.neighbor[socks]
                            continue

                #################
                # send my message
                #################
                else:
                    # If we are sending video, we should not sent other message
                    if self.VIDEOSENDING == 0:
                        message = sys.stdin.readline()[:-1]
                        # except:
                        #     # self.removeNode()
                        #     parent.close()
                        #     server.close()
                        #     sys.exit()
                        if message == ":q":
                            sys.stdout.write("\033[A")
                            self.removeNode()
                            # self.parent.close()
                            # self.server.close()
                            os._exit(0)
                        elif message == ":v":
                            # video_send: choose a target to video
                            sys.stdout.write("\033[A")
                            # sys.stdout.write("Choose the one you want to video chat with:")
                            print("Choose the one you want to video chat with:")
                            index = 0
                            for node in self.neighbor.keys():
                                print(index,":",node)
                                index += 1
                            selected_index = int(sys.stdin.readline()[:-1])
                            while selected_index > len(list(self.neighbor.keys())):
                                sys.stdout.write("[Exception] index out of range, please rechoose")
                                selected_index = int(sys.stdin.readline()[:-1])
                            selected_sockets = list(self.neighbor.keys())[selected_index]
                            selected_sockets.send(VIDEOMODEINIT.encode())
                            self.VIDEOSENDING = 1
                            sys.stdout.write("You've sent a video chat request.")
                            sys.stdout.flush()
                        # BUG found: deadlock, need fix
                        else:
                            for node in self.neighbor.keys():
                                node.send(message.encode())
                            sys.stdout.write("\033[A")
                            sys.stdout.write("<You> ")
                            print(message)
                            sys.stdout.flush()


    """
    removeNode(self):
        DESCRIPTION: handles a node going offline
        INPUT: self: node instance
        OUTPUT: NONE
        SIDEEFFECTS: tells all neighbors to reconnect to another node (one of
                     the neighbors)
    """
    def removeNode(self):
        print(">> Exiting program...")
        count = 0
        if len(self.neighbor) != 1 and len(self.neighbor) != 0:
            for i in self.neighbor.keys():
                if count != 0:
                    i.send(RECONNECT.encode())
                    i.recv(SIG_LENGTH)
                    message = self.neighbor[p][0] + " " + self.neighbor[p][1]
                    i.send(message.encode())
                else:
                    p = i
                count += 1

    """
    recvNode():
        DESCRIPTION: node constructor
        INPUT: self: node instance
               ip: IP address of current PC
               port: port number of server socket
        OUTPUT: NONE
        SIDEEFFECTS: connect to a network. Start threads to receive connection
                     requests and to handle message communications
    """
    def __init__(self, ip, port):
        self.data = b''
        self.VIDEORSV = 0
        self.VIDEOSENDING = 0
        self.video_receive_sockets = []
        self.video_send_sockets = []
        sys.stdout.write(">> Enter IP address of target node:\n")
        sys.stdout.write("   (Press enter if this is the first node)\n")
        sys.stdout.write(">> IP address: ")
        sys.stdout.flush()
        ip_temp = sys.stdin.readline()[:-1]
        sys.stdout.write(">> Enter port number of target node:\n")
        sys.stdout.write("   (Enter 0 if this is the first node)\n")
        sys.stdout.write(">> Port: ")
        sys.stdout.flush()
        while True:
            try:
                port_temp = int(sys.stdin.readline()[:-1])
                break
            except:
                sys.stdout.write(">> Please input a integer number:\n")
                sys.stdout.write(">> Port: ")
                sys.stdout.flush()
                continue

        if ip_temp != "" and port_temp != 0:
            while True:
                if ip_temp != "" and port_temp != 0:
                    try:
                        self.parent.connect((ip_temp, port_temp))
                    except:
                        sys.stdout.write(">> [Exception: Connection failed!] \n")
                        sys.stdout.write(">> Re-enter IP address of target node:\n")
                        sys.stdout.write("   (Press enter if this is the first node)\n")
                        sys.stdout.write(">> IP address: ")
                        sys.stdout.flush()
                        ip_temp = sys.stdin.readline()[:-1]
                        sys.stdout.write(">> Re-enter port number of target node:\n")
                        sys.stdout.write("   (Enter 0 if this is the first node)\n")
                        sys.stdout.write(">> Port: ")
                        sys.stdout.flush()
                        port_temp = int(sys.stdin.readline()[:-1])
                        continue
                    self.parent.send(str(port).encode())
                    self.neighbor[self.parent] = [ip_temp,str(port_temp)]
                    break
                else:
                    break

        # start sender thread and receive connect request
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.IP_address = ip
        self.Port = port
        self.server.bind((self.IP_address, self.Port))
        self.server.listen(100) # allow a maximum of 100 nodes
        self.render = 0
        sys.stdin.flush()

        self.recvThread = threading.Thread(target = self.recvNode)
        self.recvThread.start()
        # self.nodesThread = threading.Thread(target = self.nodeThread)
        # self.nodesThread.start()
        # self.video_render()
        self.nodeThread()

"""
main:
    declares a node instance
"""
if __name__== "__main__":
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        sys.exit()
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    me = node(IP_address, Port)
