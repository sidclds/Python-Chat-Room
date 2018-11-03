#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import getpass
import random
import time
import os
try:
    os.system("title sidclds Chat Server")
except:
    print("Sorry, but this code supports Windows only.")
    time.sleep(5)
    os._exit(0)
admincode = raw_input("What is the admin code for this server: ")
clients = {}
addresses = {}
admin = getpass.getuser()
HOST = '127.0.0.1'
PORT = random.randint(1, 65535)
strport = PORT
strhost = HOST
print("Host: " + str(strhost))
print("Port: " + str(strport))
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("")
        print("%s:%s has connected." % client_address)
        print("")
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = getpass.getuser()
    welcome = 'Welcome %s! Type {exit} to exit, and {help} for help!' % name
    client.send(bytes(welcome))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg))
    clients[client] = name
    while True:
        try:
            msg = client.recv(BUFSIZ)
        except:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name))
            break
        if msg == bytes("{exit}"):
            client.send(bytes("{exit}"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name))
            break
        elif msg == bytes("{help}"):
            print("  %s: {help}") % name
            client.send(bytes("Info:"))
            time.sleep(0.1)
            client.send(bytes("If you type a command wrong, it will not be sent to the"))
            time.sleep(0.1)
            client.send(bytes("other users"))
            time.sleep(0.1)
            client.send(bytes("User commands:"))
            time.sleep(0.1)
            client.send(bytes("{quit} -- client quits server"))
            time.sleep(0.1)
            client.send(bytes("{help} -- brings up list of commands"))
            time.sleep(0.1)
            client.send(bytes("Admin commands:"))
            time.sleep(0.1)
            client.send(bytes("{serverterminate@(Insert admin code here)} -- Terminates"))
            time.sleep(0.1)
            client.send(bytes("server"))
        elif msg == bytes("{serverterminate@" + admincode + "}"):
            broadcast(bytes("Server: {terminate}"))
            print("")
            os._exit(0)
        else:
            broadcast(msg, name+": ")
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    name = getpass.getuser()
    if not msg[0] == "{":
        for sock in clients:
            sock.send(bytes(prefix)+msg)
        print("  " + bytes(prefix)+msg)
        
haveVar=0   
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
