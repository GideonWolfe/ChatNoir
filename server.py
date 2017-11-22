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
nickDictionary = {}



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
    nickDictionary[address[0]] = address[0]
    # Loop running to handle he client
    while True:

        # Keep trying to listen for incoming data
        try:
            data = conn.recv(2048)

            # If we receive data, decode it
            if data:
                data = bytes.decode(data)

                if data[0] == "/":
                    if data[:5] == "/nick":
                        if data[6:-1] in nickDictionary.values():
                            error = "[INFO] Username already registered"
                            error = str.encode(error)
                            conn.send(error)
                        else:
                            nickName = data[6:-1]
                            confirmation = "[INFO] Your nickname is now "+nickName
                            confirmation = str.encode(confirmation)
                            print("[INFO] "+address[0]+" is now known as "+nickName)
                            nickDictionary[address[0]] = nickName
                            conn.send(confirmation)
                            notification = ("[INFO] "+address[0]+" is now known as "+nickName)
                            broadcast(notification, conn)

                    elif data[:5] == "/exit":
                        print("[INFO] Closing connection of " + address[0])
                        disCommand = "disconnected"
                        disCommand = str.encode(disCommand)
                        conn.send(disCommand)
                        conn.close()
                        connectionList.remove(conn)
                        broadcastMessage = "[INFO] "+nickDictionary[address[0]]+" has left the room."
                        broadcast(broadcastMessage, conn)


                else:
                    broadcastMessage = ("< "+str(nickDictionary[address[0]])+" > : "+str(data))
                    print(broadcastMessage)
                    broadcast(broadcastMessage, conn)

            # If not, there is a broken connection.
            else:
                print("[INFO] Closing connection of "+address[0])
                conn.close()
                connectionList.remove(conn)
        except:
            continue


# Listens for op commands
def listenLocal():
    while True:
        servCommand = sys.stdin.readline()

        if servCommand[:6] == "/whois":
            user = servCommand[7:-1]
            for ip, nick in nickDictionary.items():
                if nick == user:
                    print("[INFO] " + user + " is " + ip)

        else:
            continue

# Start listening for keyboard input
localListenerThread = threading.Thread(target=listenLocal)
localListenerThread.daemon = True
localListenerThread.start()

# The main loop in charge of server processes
while True:
    conn, address = server.accept()
    connectionList.append(conn)
    connectionThread = threading.Thread(target=handler, args=(conn, address))
    connectionThread.daemon = True
    connectionThread.start()




