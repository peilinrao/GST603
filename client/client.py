import socket
import select
import sys
import getpass
import time
from time import sleep

FILE_NO_EXIST = "\b\b"
FILE_UPLOADING = "\0\0"
FILE_REQUEST = "\n\n"
EOF = "\0\0\0"
DONE = "\n\n\n"
FAIL = "\b\b\b"
NO_EXIST = "\b\0"
FILEMODE = False

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
            server.send("\b")
            print ">> Creating new user... (Do not use :S as user name!!)"
            create()
            return
        password = getpass.getpass(prompt='>> Password: ')
        server.send(usrName[:-1] + " " + password)
        message = server.recv(200)
        if message == "\b":
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
        print ">> This is an invalid username!"
        sys.stdout.write(">> Username: ")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
    password = getpass.getpass(prompt='>> Password: ')
    server.send(usrName[:-1] + " " + password)

'''
receiveFile(name):
DESCRIPTION: receive a file from client
INPUT:       conn: socket of the client
             addr: IP address of the client
             name: name of the uploaded file
OUTPUT:      none
SIDEEFFECTS: store the uploaded file in cloud server. Notice the sender once
             done. Notice other users about arrival of a file.
'''
def receiveFile(name):
    f = open(name, "wb")
    package = server.recv(2048)
    server.send(DONE)
    while package[0] == "\b":
        f.write(package[1:])
        # print package
        package = server.recv(2048)
        server.send(DONE)

    f.close()
    print name + " has been successfully downloaded"

    # server.send(DONE)

'''
sendFile(f):
DESCRIPTION: upload file to server
INPUT:       file handler
OUTPUT:      none
SIDEEFFECTS: upload the file to server
'''
def sendFile(f):
    try:
        package = f.read(1024)
        while package:
            server.send("\b"+package)
            package = f.read(1024)
            server.recv(10)

        server.send(EOF)
        server.recv(10)
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
    local_net_setting_created = 0

    try:
        with open("local_net_setting.txt") as f:
            lines = f.readlines()
        local_net_setting_created = 1
        index = int(lines[0])
        if(len(lines) < 3):
            raise IOError
        sys.stdout.write(">> Do you want to use the default IP address and port? \n")
        sys.stdout.write(">> Yes(Y)/No(N): ")
        sys.stdout.flush()
        answer = sys.stdin.readline()[:-1]
        # Assume user is kind
        if answer == "Y":
            IP_address = str(lines[1 + index * 2][:-1])
            Port = int(lines[2 + index * 2])
            server.connect((IP_address, Port))
        elif answer == "N":
            raise IOError
    except:
        #with open("local_net_setting.txt", "w") as f:
        #    f.writelines(lines)
        f = open("local_net_setting.txt", "a+")
        if local_net_setting_created == 0:
            f.write("0\n")
            local_net_setting_created = 1
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
                server.connect((ip_temp, port_temp))
            except:
                # print(ip_temp, port_temp)
                sys.stdout.write(">> [Exception: Please enter the valid IP address and port!] \n")
                continue
            f.write(ip_temp+"\n")
            f.write(str(port_temp)+"\n")
            IP_address = ip_temp
            Port = port_temp
            break
        f.close()

        #updating the index
        with open("local_net_setting.txt") as f:
            lines = f.readlines()
        lines[0] = str(len(lines)/2 - 1)+"\n"
        # print lines
        with open("local_net_setting.txt", "w") as f:
            f.writelines(lines)

    #IP_address = str(sys.argv[1])
    #Port = int(sys.argv[2])

    print ">> Welcome to GST603 Chatroom!"
    login()
    while True:
        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                if message == "\n" or message == "\b" or message == "\0":
                    continue
                print message
            else:
                message = sys.stdin.readline()

                if FILEMODE:
                    if message == ":q\n":  # quit the chatroom
                        server.close()
                        sys.exit()
                    elif message == ":uf\n":  # upload file
                        print ">> Type in the file name you want to upload: (please include the entire directory)"
                        sys.stdout.flush()
                        file_dir = sys.stdin.readline()[:-1]
                        fileName = file_dir.split("/")
                        # print file_dir
                        try:
                            f = open(file_dir, "rb")
                            server.send(FILE_UPLOADING)
                            sleep(0.01)
                            server.send(fileName[-1])
                            sleep(0.01)
                            sendFile(f)
                            f.close()
                        except:
                            print ">> No such file."
                            f.close()

                    elif message == ":df\n":  # download file from cloud
                        server.send(FILE_REQUEST)
                        message = server.recv(2048)
                        server.send(DONE)
                        print ">> Please choose one file to donwload:\n" + message
                        sys.stdout.flush()
                        fileName = sys.stdin.readline()[:-1]      # read the file name and send to the server
                        server.send(fileName)
                        message = server.recv(3)
                        if message == DONE:
                            receiveFile(fileName)
                        else:
                            print ">> File reception failed :(" + message
                    elif message == ":h\n":  # user want help
                        print '''>> ":S": register (can only be used when login)\n>> ":uf": upload file to the server\n>> ":df": download file from the server\n>>":q": quit the chatroom.\n'''
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
                        print '''>> ":S": register (can only be used when login)\n>>":q": quit the chatroom.\n'''
                    else:
                        server.send(message[:-1])
                        sys.stdout.write("\033[A")
                        sys.stdout.write("<You> ")
                        sys.stdout.write(message)
                        sys.stdout.flush()


    server.close()

if __name__== "__main__":
    main()
