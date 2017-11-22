# Author: Gideon Wolfe
# Class: CSCI 141
# Assignment: Final Project

import socket
import sys
import threading

print(" _______           _______ _________ _        _______ _________ _______")
print("(  ____ \|\     /|(  ___  )\__   __/( (    /|(  ___  )\__   __/(  ____ )")
print("| (    \/| )   ( || (   ) |   ) (   |  \  ( || (   ) |   ) (   | (    )| ")
print("| |      | (___) || (___) |   | |   |   \ | || |   | |   | |   | (____)| ")
print("| |      |  ___  ||  ___  |   | |   | (\ \) || |   | |   | |   |     __) ")
print("| |      | (   ) || (   ) |   | |   | | \   || |   | |   | |   | (\ (    ")
print("| (____/\| )   ( || )   ( |   | |   | )  \  || (___) |___) (___| ) \ \__ ")
print("(_______/|/     \||/     \|   )_(   |/    )_)(_______)\_______/|/   \__/ ")
print("__________________________________________________________________________")

# Declaring variables
serverIP = str(sys.argv[1])
serverPort = int(sys.argv[2])

# If client enters incompatible arguments
if len(sys.argv) > 3:
    print("Correct usage: \"client.py <server IP> <server port>\"")
    exit()

# Setting up client connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((serverIP, serverPort))
server.setblocking(True)
print("[INFO] Connecting to "+serverIP+" on port "+str(serverPort))
print("[INFO] Connection success!")


def listenLocal():
    while True:
        message = sys.stdin.readline()
        msgToSend = str.encode(message)
        server.send(msgToSend)
        if message[0] != "/":
            #sys.stdout.write("<You> ")
            #sys.stdout.write(message)
            sys.stdout.flush()
        else:
            continue

def listenServer():
    while True:
            message = server.recv(2048)
            if message:
                message = bytes.decode(message)
                print(message)
                sys.stdout.flush()
                if message == "disconnected":
                    print("[INFO] Exiting...")
                    sys.exit()

            else:
                server.close()

# Start listening for keyboard input
localListenerThread = threading.Thread(target=listenLocal)
localListenerThread.daemon = True
localListenerThread.start()

# Start listening for messages from the server
serverListenerThread = threading.Thread(target=listenServer)
serverListenerThread.daemon = False
serverListenerThread.start()
serverListenerThread.join()