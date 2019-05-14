import socket
import select
from thread import *
import sys

FILE_NO_EXIST = "\b\b"
FILE_UPLOADING = "\0\0"
FILE_REQUEST = "\n\n"
EOF = "\0\0\0"
DONE = "\n\n\n"

list_of_clients = []
cloud_files = []
user_name_dict = {}
user_data_dict = {}

def receiveFile(conn, addr, name):
    f = open(name, "wb")
    package = conn.recv(2048)
    conn.send(DONE)
    while package[0] == "\b":
        f.write(package[1:])
        # print package
        package = conn.recv(2048)
        conn.send(DONE)

    f.close()

    # update the directory
    if name not in cloud_files:
        f = open("cloudFileDir.txt", "a+")
        f.write(name + "\n")
        f.close()
        cloud_files.append(name)
    print "\n" + user_name_dict[conn] + " has uploaded " + name + " to cloud.\n"
    broadcast("\n" + user_name_dict[conn] + " has uploaded " + name + " to cloud.\n", conn) # tell all clients a cloud file has been uploaded
    conn.send("\nFile uploaded")

def sendFile(conn, addr, name):
    try:
        f = open(name, "rb")
        while True:
            package = f.read(2048)

            if not package:  # done reading
                break

            conn.send(package)

        f.close()

    except:
        conn.send(FILE_NO_EXIST)


def clientthread(conn, addr):
    conn.send("Welcome to GST603 Chatroom, " + user_name_dict[conn] + "!\n:q to quit the chatroom, :uf to upload cloud files:)")
    broadcast_m = "\n" + user_name_dict[conn] + " has entered chatroom.\n"
    broadcast(broadcast_m, conn)
    conn.send("\0")
    #sends a message to the client whose user object is conn
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    if message == FILE_UPLOADING: # a file is being uploaded
                        try:
                            fileName = conn.recv(2048) # read the file name
                            receiveFile(conn, addr, fileName)
                        except:
                            continue
                    elif message == FILE_REQUEST: # the client wants the file
                        # give user the cloud file directory
                        print "Choose from cloud file blow:"
                        try:
                            f = open("cloudFileDir.txt", "r")
                            try:
                                message = conn.recv(1024)
                                if message:
                                    sendFile(conn, addr, name)
                                else:
                                    remove(conn)
                            except:
                                continue
                        except:
                            f.close()
                            conn.send(FILE_NO_EXIST)  # no cloud file available
                    else:
                        print "<" + user_name_dict[conn] + "> " + message
                        message_to_send = "<" + user_name_dict[conn] + "> " + message
                        broadcast(message_to_send,conn)
                        #prints the message and address of the user who just sent the message on the server terminal

                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        broadcast_m = "\nUser " + user_name_dict[connection] + " exited the chatroom.\n"
        print broadcast_m
        broadcast(broadcast_m,connection)
        list_of_clients.remove(connection)
        user_name_dict.remove(connection)


def readUsrData(input):
    try:
        f = open(input, "r")
    except:
        f = open(input, "a+")
        f.close()
        return

    for line in f.readlines():
        temp = line.split()
        user_data_dict[temp[0]] = temp[1]

    # print user_data_dict

    f.close()

def txtToList(input, list):
    try:
        f = open(input, "r")
    except:
        return

    for line in f.readlines():
        list.append(line[:-1])

    # print user_data_dict

    f.close()

def createNewUsr(input, name, password):
    try:
        f = open(input, "a+")
    except:
        f.close()
        return

    f.write(name + " " + password + "\n")
    readUsrData(input)

    f.close()

def registerpolling(conn,addr):
    # print "Creating new user...\n"
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    temp = message.split()
                    createNewUsr("user_data.txt", temp[0], temp[1])
                    list_of_clients.append(conn)
                    user_name_dict[conn] = temp[0]
                    start_new_thread(clientthread,(conn,addr))
                    print temp[0] + " created and enters the chatroom\n"
                    #prints the message and address of the user who just sent the message on the server terminal
                    return
                else:
                    remove(conn)
            except:
                continue

def signinpolling(conn, addr):
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    if message != "\b":
                        temp = message.split()
                        if temp[0] in user_data_dict:
                            if temp[1] == user_data_dict[temp[0]]:
                                list_of_clients.append(conn)
                                user_name_dict[conn] = temp[0]
                                start_new_thread(clientthread,(conn,addr))
                                print temp[0] + " enters the chatroom\n"
                                #prints the message and address of the user who just sent the message on the server terminal
                                return
                            else:
                                conn.send("\b")
                                print "Password not correct for " + temp[0] + "\n"
                                continue
                        else:
                            conn.send("\n")
                            list_of_clients.remove(conn)
                            print "No existing user.\n"
                            continue
                    else:
                        start_new_thread(registerpolling,(conn,addr))
                        return
                else:
                    remove(conn)
            except:
                continue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
readUsrData("user_data.txt")
txtToList("cloudFileDir.txt", cloud_files)
print "GST603 server booted!"

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """

    # check for log in

    print "\n" + addr[0] + " connected"
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    message = conn.recv(200)
    if message:
        if message != "\b":
            temp = message.split()
            if temp[0] in user_data_dict:
                if temp[1] == user_data_dict[temp[0]]:
                    list_of_clients.append(conn)
                    user_name_dict[conn] = temp[0]
                    start_new_thread(clientthread,(conn,addr))
                    print temp[0] + " enters the chatroom\n"

                    #creates and individual thread for every user that connects
                else:
                    conn.send("\b")
                    print "Password not correct for " + temp[0] + "\n"
                    start_new_thread(signinpolling,(conn,addr))
            else:
                conn.send("\n")
                print "No existing user.\n"
                start_new_thread(signinpolling,(conn,addr))
        else:
            start_new_thread(registerpolling,(conn,addr))


conn.close()
server.close()