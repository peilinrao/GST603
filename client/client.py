import socket
import select
import sys
import getpass
import time
from time import sleep

# constants
FILE_NO_EXIST = "\b\b"
FILE_UPLOADING = "\0\0"
FILE_REQUEST = "\n\n"
EOF = "\0\0\0"
DONE = "\n\n\n"
FAIL = "\b\b\b"
NO_EXIST = "\b\0"
NEW_USR = "\0\b"
PASS_ERR = "\b"
FILE_REMOVE = "\b\0\b"
MSG_BUF_SIZE = 2048
PKG_SIZE = 4*2048
SIG_LENGTH = 128
FILEMODE = True

# Global
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def readNetSettings(input):
    try:
        f = open(input, "r")
    except:
        setupNetwork(input)
        return

    for line in f.readlines():
        temp = line.split()


    # print user_data_dict
    f.close()

'''
login():
DESCRIPTION: for user login purpose, check for validity of user credentials
INPUT:       none
OUTPUT:      none
SIDEEFFECTS: instructions for users to login correctly are printed on terminal
             allow new user registration
'''
def login():
    while True:
        sys.stdout.write(">> Please login. To register, type in :S.\n")
        sys.stdout.write(">> Username: ")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
        if usrName == ":S\n":
            server.send(NEW_USR)
            print ">> Creating new user... (Do not use :S as Username!!)"
            create()
            return
        password = getpass.getpass(prompt='>> Password: ')
        server.send(usrName[:-1] + " " + password)
        message = server.recv(200)
        if message == PASS_ERR:
            print ">> Password incorrect."
            continue
        elif message == NO_EXIST:
            print ">> User doesnot exist."
            continue
        else:
            print message
            return

'''
create():
DESCRIPTION: create a new user
INPUT:       none
OUTPUT:      none
SIDEEFFECTS: instructions for users to register correctly are printed on
             terminal. enter the chatroom once registration is done
'''
def create():
    sys.stdout.write(">> Username: ")
    sys.stdout.flush()
    usrName = sys.stdin.readline()
    while usrName == ":S\n":
        print ">> This is an invalid Username!"
        sys.stdout.write(">> Username: ")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
    password = getpass.getpass(prompt='>> Password: ')
    server.send(usrName[:-1] + " " + password)

    while server.recv(SIG_LENGTH) == FAIL:
        print ">> This Username is already taken, please use another one."
        sys.stdout.write(">> Username: ")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
        while usrName == ":S\n":
            print ">> This is an invalid Username!"
            sys.stdout.write(">> Username: ")
            sys.stdout.flush()
            usrName = sys.stdin.readline()
        password = getpass.getpass(prompt='>> Password: ')
        server.send(usrName[:-1] + " " + password)

'''
receiveFile(name):
DESCRIPTION: receive a file from server
INPUT:       name: name of the uploaded file
OUTPUT:      none
SIDEEFFECTS: store the uploaded file in cloud server. Notice the sender once
             done. Notice other users about arrival of a file.
'''
def receiveFile(name):
    f = open(name, "wb")
    package = server.recv(2*PKG_SIZE)

    server.send(DONE)
    while True:
        # print("Hey")
        f.write(package)
        # print len(package)
        package = server.recv(2*PKG_SIZE)
        server.send(DONE)

        if package == EOF:
            break
    # for c in package:
    #    print ord(c)

    f.close()
    server.send(EOF)
    print name + " has been successfully downloaded"

    # server.send(DONE)

'''
receiveFile():
DESCRIPTION: remove a file from the server
INPUT:       none
OUTPUT:      none
SIDEEFFECTS: remove a file from the server
'''
def removeFile():
    message = server.recv(MSG_BUF_SIZE)
    if message == FAIL:
        return
    else:
        print ">> Choose one from the following files to remove from cloud:"
        print message
        sys.stdout.flush()
        message = sys.stdin.readline()[:-1]
        server.send(message)
        message = server.recv(SIG_LENGTH)
        if message == FAIL:
            print ">> File failed to remove."
        else:
            print ">> File successfully removed."

'''
sendFile(f):
DESCRIPTION: upload file to server
INPUT:       file handler
OUTPUT:      none
SIDEEFFECTS: upload the file to server
'''
def sendFile(f):
    message = server.recv(SIG_LENGTH)
    if message == FAIL:
        print ">> File with the same name is already uploaded by other user. Rename the file and try again."
        return
    elif message == FILE_REMOVE:
        sys.stdout.write(">> You have already uploaded a file with the same name. Do you want to overwrite the old file? (Y/N) ")
        sys.stdout.flush()
        message = sys.stdin.readline()[:-1]

        # sanity check
        while message != 'Y' and message != 'N':
            sys.stdout.write(">> Invalid input. Please select (Y) or (N): ")
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

        if message == 'Y':
            server.send(DONE)
        else:
            server.send(FAIL)
            print ">> You have aborted uploading process."
            return

    try:
        package = f.read(PKG_SIZE)
        while package:
            server.send(package)
            package = f.read(PKG_SIZE)
            server.recv(SIG_LENGTH)

        while server.send(EOF) != len(EOF):
            continue

        print ">> File uploaded."
    except:
        print ">> [ERROR: Cannot upload file.] "
        return

'''
main():
DESCRIPTION: main body of chatroom client codes
INPUT:       none
OUTPUT:      none
SIDEEFFECTS: Start the program. Set up internet connection. Let user login,
             handle incoming messages and send message to server.
'''
def main():

    try:
        with open("local_net_setting.txt") as f:
            lines = f.readlines()
        if(len(lines)<2):
            raise IOERROR
        sys.stdout.write(">> Do you want to use the default IP address and port? \n")
        sys.stdout.write(">> Yes(Y)/No(N): ")
        sys.stdout.flush()
        answer = sys.stdin.readline()[:-1]
        # sanity check
        while answer != 'Y' and answer != 'N':
            sys.stdout.write(">> Invalid input. Please select (Y) or (N): ")
            sys.stdout.flush()
            answer = sys.stdin.readline()[:-1]

        if answer == "Y":
            IP_address = str(lines[0][:-1])
            Port = int(lines[1])
            print(">> Trying to connect.")
            server.connect((IP_address, Port))
            print(">> Connected!")
        elif answer == "N":
            raise IOError
    except:
        f = open("local_net_setting.txt", "w")
        while True:
            sys.stdout.write(">> Enter the IP address you want to connect to: \n")
            sys.stdout.write(">> IP address: ")
            sys.stdout.flush()
            ip_temp = sys.stdin.readline()[:-1]
            sys.stdout.write(">> Enter the port you want to connect to: \n")
            sys.stdout.write(">> Port: ")
            sys.stdout.flush()
            port_temp = int(sys.stdin.readline()[:-1])
            try:
                print(">> Trying to connect.")
                server.connect((ip_temp, port_temp))
                print(">> Connected!")
            except:
                # print(ip_temp, port_temp)
                sys.stdout.write(">> [Exception: Connection failed!] \n")
                continue
            print(">> Do you want to save yout IP and Port configuration?")
            sys.stdout.write(">> Yes(Y)/No(N): ")
            sys.stdout.flush()
            answer = sys.stdin.readline()[:-1]
            # sanity check
            while answer != 'Y' and answer != 'N':
                sys.stdout.write(">> Invalid input. Please select (Y) or (N): ")
                sys.stdout.flush()
                answer = sys.stdin.readline()[:-1]

            if answer == "Y":
                f.write(ip_temp+"\n")
                f.write(str(port_temp)+"\n")
            break
        f.close()

    print ">> Welcome to GST603 Chatroom!"
    login()
    while True:
        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(MSG_BUF_SIZE)
                if message[0] == "\n" or message[0] == "\b" or message[0] == "\0":
                    continue
                print message
            else:
                message = sys.stdin.readline()

                if FILEMODE:
                    if message == ":q\n":  # quit the chatroom
                        server.close()
                        sys.exit()
                    elif message == ":uf\n":  # upload file
                        print ">> Type in the file name you want to upload:"
                        sys.stdout.flush()
                        file_dir = sys.stdin.readline()[:-1]
                        fileName = file_dir.split("/")
                        # print file_dir
                        try:
                            f = open(file_dir, "rb")
                            server.send(FILE_UPLOADING)
                            server.recv(SIG_LENGTH)
                            server.send(fileName[-1])
                            server.recv(SIG_LENGTH)
                            sendFile(f)
                            f.close()
                        except:
                            print ">> No such file."
                            f.close()

                    elif message == ":df\n":  # download file from cloud
                        server.send(FILE_REQUEST)
                        message = server.recv(MSG_BUF_SIZE)
                        # server.send(DONE)
                        print ">> Please choose one file to download:\n" + message
                        sys.stdout.flush()
                        fileName = sys.stdin.readline()[:-1]      # read the file name and send to the server
                        server.send(fileName)
                        message = server.recv(SIG_LENGTH)
                        if message == DONE:
                            receiveFile(fileName)
                        else:
                            print ">> File reception failed :(" + message
                    elif message == ":rf\n":  # user want to remove a self uploaded file from server
                        server.send(FILE_REMOVE)
                        message = server.recv(SIG_LENGTH)
                        server.send(DONE)
                        if message == FAIL:
                            print ">> There are no files uploaded by you on cloud."
                        else:
                            removeFile()
                    elif message == ":h\n":  # user want help
                        print '''>> [help]\n>> ":S": register (can only be used when login)\n>> ":uf": upload file to the server\n>> ":df": download file from the server\n>> ":rf": remove a file uploaded by you\n>> ":q": quit the chatroom.\n'''
                    else:
                        server.send(message[:-1])
                        sys.stdout.write("\033[A")
                        sys.stdout.write("<You> ")
                        sys.stdout.write(message)
                        sys.stdout.flush()
                else:
                    if message == ":q\n":  # quit the chatroom
                        server.close()
                        sys.exit()
                    elif message == ":h\n":  # user want help
                        print '''>> [help]\n>> ":S": register (can only be used when login)\n>> ":q": quit the chatroom.\n'''
                    else:
                        server.send(message[:-1])
                        sys.stdout.write("\033[A")
                        sys.stdout.write("<You> ")
                        sys.stdout.write(message)
                        sys.stdout.flush()


    server.close()

if __name__== "__main__":
    main()
