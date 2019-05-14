import socket
import select
from thread import *
import sys

# constants
FILE_NO_EXIST = "\b\b"
FILE_UPLOADING = "\0\0"
FILE_REQUEST = "\n\n"
EOF = "\0\0\0"
DONE = "\n\n\n"
FAIL = "\b\b\b"
NO_EXIST = "\b\0"
FILEMODE = False

# globals
list_of_clients = []
cloud_files = []
user_name_dict = {}
user_data_dict = {}

'''
receiveFile(conn, addr, name):
DESCRIPTION: receive a file from client
INPUT:       conn: socket of the client
             addr: IP address of the client
             name: name of the uploaded file
OUTPUT:      none
SIDEEFFECTS: store the uploaded file in cloud server. Notice the sender once
             done. Notice other users about arrival of a file.
'''
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
    message = "\n" + user_name_dict[conn] + " has uploaded " + name + " to cloud.\n"
    print message

    broadcast(message, conn) # tell all clients a cloud file has been uploaded
    conn.send(DONE)

'''
sendFile(f, conn):
DESCRIPTION: upload file to server
INPUT:       file handler
OUTPUT:      none
SIDEEFFECTS: upload the file to server
'''
def sendFile(f, conn):
    try:
        package = f.read(1024)
        while package:
            conn.send("\b"+package)
            package = f.read(1024)
            conn.recv(10)

        conn.send(EOF)
        print ">> File downloaded by " + user_name_dict[conn]+ "."
    except:
        print ">> [Error: file cannot be uploaded.]"
        return

'''
clientthread(conn, addr):
DESCRIPTION: a thread for client on the server
INPUT:       conn: socket of the client
             addr: IP address of the client
OUTPUT:      none
SIDEEFFECTS: check for client activities on the server, including messages,
             file sending request and file downloading request
'''
def clientthread(conn, addr):
    conn.send(">> Welcome to GST603 Chatroom, " + user_name_dict[conn] + """! Type ":h" for help!""")
    broadcast_m = ">> " + user_name_dict[conn] + " has entered chatroom."
    broadcast(broadcast_m, conn)
    conn.send("\0")
    #sends a message to the client whose user object is conn
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    if FILEMODE:
                        if message == FILE_UPLOADING: # a file is being uploaded
                            try:
                                fileName = conn.recv(2048) # read the file name
                                receiveFile(conn, addr, fileName)
                            except:
                                continue
                        elif message == FILE_REQUEST: # the client wants the file
                            # give user the cloud file directory
                            print ">> User requesting file..."
                            try:
                                message = ""
                                for elements in cloud_files:
                                    message += elements + "\n"
                                try:
                                    conn.send(message)
                                    message = conn.recv(3)    # wait for response
                                    message = conn.recv(1024)
                                    if message:
                                        try:
                                            f = open(message, "rb")
                                            conn.send(DONE)
                                            sendFile(f, conn)
                                            f.close()
                                        except:
                                            conn.send(FAIL)
                                            f.close()
                                    else:
                                        remove(conn)
                                except:
                                    continue
                            except:
                                conn.send(FILE_NO_EXIST)  # no cloud file available
                        else:
                            if message[0] == "\n" and message[1] == "\n":
                                continue
                            message_to_send = "<" + user_name_dict[conn] + "> " + message
                            print message_to_send
                            broadcast(message_to_send,conn)
                            #prints the message and address of the user who just sent the message on the server terminal
                    else:
                        if message[0] == "\n" and message[1] == "\n":
                            continue
                        message_to_send = "<" + user_name_dict[conn] + "> " + message
                        print message_to_send
                        broadcast(message_to_send,conn)
                else:
                    remove(conn)
            except:
                continue

'''
broadcast(message,connection):
DESCRIPTION: broadcast a message
INPUT:       message: the message need broadcasting
             connection: socket of the sender
OUTPUT:      none
SIDEEFFECTS: send message to all other clients except the sender
'''
def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                print ">> [Exception: cannot broadcast]"

                remove(clients)

'''
remove(connection):
DESCRIPTION: remove a user from online list
INPUT:       connection: socket of the client
OUTPUT:      none
SIDEEFFECTS: remove a user from online list
'''
def remove(connection):
    if connection in list_of_clients:
        broadcast_m = ">> User " + user_name_dict[connection] + " exited the chatroom."
        print broadcast_m
        broadcast(broadcast_m,connection)
        list_of_clients.remove(connection)
        user_name_dict.remove(connection)

'''
readUsrData(input):
DESCRIPTION: read user_data
INPUT:       input: name of the file
OUTPUT:      none
SIDEEFFECTS: read user credentials from a txt file into user_data_dict
'''
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

'''
txtToList(input, list):
DESCRIPTION: convert txt file into a list
INPUT:       input: name of the file
             list: name of the output list
OUTPUT:      none
SIDEEFFECTS: convert txt file into a list line by line (list include no "\n")
'''
def txtToList(input, list):
    try:
        f = open(input, "r")
    except:
        return

    for line in f.readlines():
        list.append(line[:-1])

    # print user_data_dict

    f.close()

'''
createNewUsr(input, name, password):
DESCRIPTION: create a new user
INPUT:       input: name of the save file
             name: user name
             password: user password
OUTPUT:      none
SIDEEFFECTS: create a new user in server data base, called by registerpolling
'''
def createNewUsr(input, name, password):
    try:
        f = open(input, "a+")
    except:
        f.close()
        return

    f.write(name + " " + password + "\n")
    readUsrData(input)

    f.close()

'''
registerpolling(conn,addr):
DESCRIPTION: deal with user registration
INPUT:       conn: socket of the new user
             addr: IP addr of the new user
OUTPUT:      none
SIDEEFFECTS: deal with user registration, created as a thread
'''
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
                    print ">> "+ temp[0] + " created and enters the chatroom\n"
                    #prints the message and address of the user who just sent the message on the server terminal
                    return
                else:
                    remove(conn)
            except:
                continue

'''
signinpolling(conn, addr):
DESCRIPTION: deal with user sign in
INPUT:       conn: socket of the user
             addr: IP addr of the user
OUTPUT:      none
SIDEEFFECTS: deal with user sign in, created as a thread
'''
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
                                print ">> "+ temp[0] + " enters the chatroom."
                                #prints the message and address of the user who just sent the message on the server terminal
                                return
                            else:
                                conn.send("\b")
                                print ">> Password not correct for " + temp[0] + "."
                                continue
                        else:
                            conn.send("\b\0")
                            list_of_clients.remove(conn)
                            print ">> No existing user.\n"
                            continue
                    else:
                        start_new_thread(registerpolling,(conn,addr))
                        return
                else:
                    remove(conn)
            except:
                continue


'''
main():
DESCRIPTION: main body of server code
INPUT:       none
OUTPUT:      none
SIDEEFFECTS: main func
'''

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
print ">> GST603 server booted!"

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """

    # check for log in

    print ">> " + addr[0] + " connected"
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
                    print ">> " + temp[0] + " enters the chatroom."

                    #creates and individual thread for every user that connects
                else:
                    conn.send("\b")
                    print ">> Password not correct for " + temp[0] + "."
                    start_new_thread(signinpolling,(conn,addr))
            else:
                conn.send("\n")
                print ">> No existing user."
                start_new_thread(signinpolling,(conn,addr))
        else:
            start_new_thread(registerpolling,(conn,addr))


conn.close()
server.close()
