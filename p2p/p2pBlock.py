"""
This is a p2p chat program.
Jun 16, 2019
Author: Jiyu Hu
"""

import threading
import socket
import select
import sys
import os

#signals used for cummunication between nodes
RECONNECT = "\0\0\0"
DONE = "\n\n\n"
#constants
MSG_BUF_SIZE = 2048
PKG_SIZE = 4*2048
SIG_LENGTH = 128
STRFORMATSIZE = 37
BINFORMATSIZE = 33

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
                if socks != sys.stdin:
                    try:
                        message = socks.recv(MSG_BUF_SIZE).decode()
                    except:
                        continue
                    if message:
                        if message == RECONNECT:
                            print(">> " + self.neighbor[socks][0] + " disconnected.")
                            socks.send(DONE.encode())
                            message = socks.recv(MSG_BUF_SIZE).decode()
                            temp = message.split()
                            socks.close()
                            del self.neighbor[socks]
                            newSocks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            newSocks.connect((temp[0], int(temp[1])))
                            self.neighbor[newSocks] = temp
                            newSocks.send(str(self.Port).encode())
                        else:
                            print('<' + self.neighbor[socks][0] + '> ' + message)
                            for node in self.neighbor.keys():
                                if node != socks:
                                    node.send(message.encode())
                    else:
                        print(">> " + self.neighbor[socks][0] + " disconnected.")
                        socks.close()
                        del self.neighbor[socks]
                        continue
                else:
                    message = sys.stdin.readline()[:-1]
                    if message != ":q":
                        for node in self.neighbor.keys():
                            node.send(message.encode())
                        sys.stdout.write("\033[A")
                        sys.stdout.write("<You> ")
                        print(message)
                        sys.stdout.flush()
                    else:
                        sys.stdout.write("\033[A")
                        self.removeNode()
                        # self.parent.close()
                        # self.server.close()
                        os._exit(0)

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
    __init__(self, ip, port):
        DESCRIPTION: node constructor
        INPUT: self: node instance
               ip: IP address of current PC
               port: port number of server socket
        OUTPUT: NONE
        SIDEEFFECTS: connect to a network. Start threads to receive connection
                     requests and to handle message communications
    """
    def __init__(self, ip, port):
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
                        while True:
                            try:
                                port_temp = int(sys.stdin.readline()[:-1])
                                break
                            except:
                                sys.stdout.write(">> Please input a integer number:\n")
                                sys.stdout.write(">> Port: ")
                                sys.stdout.flush()
                                continue
                        continue
                    self.parent.send(str(port).encode())
                    temp = []
                    temp.append(ip_temp)
                    temp.append(str(port_temp))
                    self.neighbor[self.parent] = temp
                    break
                else:
                    break

        # start sender thread and receive connect request
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.IP_address = ip
        self.Port = port
        self.server.bind((self.IP_address, self.Port))
        self.server.listen(100) # allow a maximum of 100 nodes

        sys.stdin.flush()
        self.recvThread = threading.Thread(target = self.recvNode)
        self.recvThread.start()

        self.nodesThread = threading.Thread(target = self.nodeThread)
        self.nodesThread.start()

"""
main:
    declares a node instance
"""
if __name__== "__main__":
    if len(sys.argv) != 3:
        print(">> Correct usage: script, your IP address, port number")
        sys.exit()
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    me = node(IP_address, Port)
