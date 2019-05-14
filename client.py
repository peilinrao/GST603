import socket
import select
import sys

def login():
    while True:
        sys.stdout.write("Welcome to chatroom, please login. To register, type in :S at user name.\n")
        sys.stdout.write("User name:")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
        if usrName == ":S\n":
            server.send("\b")
            print "Creating new user..."
            create()
            return
        sys.stdout.write("Password:")
        sys.stdout.flush()
        password = sys.stdin.readline()
        server.send(usrName[:-1] + " " + password[:-1])


        message = server.recv(200)
        if message == "\b":
            print "Password incorrect, please login again. Or enter :S in User name if you want to register.\n"
            continue
        elif message == "\n":
            print "User doesnot exist, please login again. Or enter :S in User name if you want to register.\n"
            continue
        else:
            print message
            return

def create():
    sys.stdout.write("User name:")
    sys.stdout.flush()
    usrName = sys.stdin.readline()
    sys.stdout.write("Password:")
    sys.stdout.flush()
    password = sys.stdin.readline()
    server.send(usrName[:-1] + " " + password[:-1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

login()
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print message
        else:
            message = sys.stdin.readline()
            if message == ":q\n":
                server.close()
                sys.exit()
            server.send(message[:-1])
            sys.stdout.write("\033[A")
            sys.stdout.write("<You> ")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
