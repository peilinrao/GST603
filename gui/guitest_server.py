import socket
import select
from _thread import *
import sys
import os
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))

server.listen(2)
print(">> test server booted!")


def clientthread(conn, addr):
    conn.send((">> Welcome to GST603 Chatroom, " + """! Type ":h" for help!""").encode())
    #sends a message to the client whose user object is conn
    while True:
        conn.send("yeah!".encode())
        sleep(2)

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """

    # check for log in

    print(">> " + addr[0] + " connected")
    # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    # Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))



conn.close()
server.close()
