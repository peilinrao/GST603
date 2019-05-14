import socket
import select
import sys
import getpass

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

def login():
    while True:
        sys.stdout.write("Please login. To register, type in :S at user name.\n")
        sys.stdout.write("User name:")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
        if usrName == ":S\n":
            server.send("\b")
            print "Creating new user... (Do not use :S as user name!!)"
            create()
            return
        # sys.stdout.write("Password:")
        # sys.stdout.flush()
        password = getpass.getpass()
        sys.stdout.write("\n")
        # print usrName[:-1] + " " + password
        server.send(usrName[:-1] + " " + password)
        message = server.recv(200)
        if message == "\b":
            print "Password incorrect, please login again. Or enter :S in User name if you want to register."
            continue
        elif message == "\n":
            print "User doesnot exist, please login again. Or enter :S in User name if you want to register."
            continue
        else:
            print message
            return

def create():
    sys.stdout.write("User name:")
    sys.stdout.flush()
    usrName = sys.stdin.readline()
    while usrName == ":S\n":
        print "This is an invalid user name!"
        sys.stdout.write("User name:")
        sys.stdout.flush()
        usrName = sys.stdin.readline()
    # sys.stdout.write("Password:")
    # sys.stdout.flush()
    password = getpass.getpass()
    sys.stdout.write("\n")
    server.send(usrName[:-1] + " " + password)

def main():
    local_net_setting_created = 0

    try:
        with open("local_net_setting.txt") as f:
            lines = f.readlines()
        local_net_setting_created = 1
        print(lines)
        index = int(lines[0])
        if(len(lines) < 3):
            raise IOError
        sys.stdout.write("Do you want to use the default IP address and port? \n")
        sys.stdout.write("Yes(Y)/No(N): ")
        sys.stdout.flush()
        answer = sys.stdin.readline()[:-1]
        # Assume user is kind
        print(answer)
        if answer == "Y":
            print("YES!")
            IP_address = str(lines[1 + index * 2][:-1])
            Port = int(lines[2 + index * 2])
            print(IP_address, Port)
            server.connect((IP_address, Port))
            print("connected!")
        elif answer == "N":
            raise IOError
        else:
            print "error"
    except:
        #with open("local_net_setting.txt", "w") as f:
        #    f.writelines(lines)
        f = open("local_net_setting.txt", "a+")
        if local_net_setting_created == 0:
            f.write("0\n")
            local_net_setting_created = 1
        while True:
            sys.stdout.write("Enter the IP address you want to connect to: \n")
            sys.stdout.write("IP address: ")
            sys.stdout.flush()
            ip_temp = sys.stdin.readline()[:-1]
            sys.stdout.write("Enter the port you want to connect to: \n")
            sys.stdout.write("Port: ")
            sys.stdout.flush()
            port_temp = int(sys.stdin.readline()[:-1])

            try:
                server.connect((ip_temp, port_temp))
            except:
                print(ip_temp, port_temp)
                sys.stdout.write("Exception: Please enter the valid IP address and port! \n")
                continue
            f.write(ip_temp+"\n")
            f.write(str(port_temp)+"\n")
            IP_address = ip_temp
            Port = port_temp
            server.connect((ip_temp, port_temp))
            break
        f.close()

        #updating the index
        with open("local_net_setting.txt") as f:
            lines = f.readlines()
        lines[0] = str(len(lines)/2 - 1)+"\n"
        print lines
        with open("local_net_setting.txt", "w") as f:
            f.writelines(lines)

    #IP_address = str(sys.argv[1])
    #Port = int(sys.argv[2])

    print "Welcome to GST603 Chatroom!"
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

if __name__== "__main__":
    main()
