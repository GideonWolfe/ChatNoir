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
print("           for Internetwork Use, Port Forwarding is Required.")

# Defining initial server parameters
sAddr = str(sys.argv[1])
sPort = int(sys.argv[2])


# Setting up server connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(True)
server.bind(('', sPort))
print("\n")
print("[INFO]: Socket bound to {} on port {}".format(sAddr, sPort))
server.listen(10)
connectionList = []

def broadcast(broadcastMessage, conn):
    for clients in connectionList:
        if clients != conn:
            try:
                broadcastMessage = str.encode(broadcastMessage)
                clients.send(broadcastMessage)
            except:
                clients.close()
                connectionList.remove(clients)

# Function that gets started on a new thread when a client connects
def handler(conn, address):

    # Establishing successful connection
    print("[INFO] "+"<"+str(address[0])+">"+" connected")
    welcome = "[INFO] Welcome to the server!"
    welcome = welcome.encode()
    conn.send(welcome)
    # Loop running to handle he client
    while True:

        # Keep trying to listen for incoming data
        try:
            data = conn.recv(2048)

            # If we receive data, broadcast it
            if data:
                data = bytes.decode(data)
                broadcastMessage = ("<"+str(address[0])+"> : "+str(data))
                print(broadcastMessage)
                broadcast(broadcastMessage, conn)

            # If not, there is a broken connection.
            else:
                print("[INFO] Closing connection of "+address[0])
                conn.close()
                connectionList.remove(conn)
        except:
            continue


# The main loop in charge of server processes
while True:
    conn, address = server.accept()
    connectionList.append(conn)
    connectionThread = threading.Thread(target=handler, args=(conn, address))
    connectionThread.daemon = True
    connectionThread.start()

