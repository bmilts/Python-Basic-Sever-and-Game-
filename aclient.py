#Admin Client TCP
import socket
import ssl
import sys

currentPlayers = " "

# Create client socket
a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ta = ssl.wrap_socket(a, certfile="100352212.crt", keyfile="100352212.key", ca_certs="5cc515-root-ca.cer")

# Connect socket to server
ta.connect(("127.0.0.1", 4001))

# Greetings Exchange
ta.sendall("Admin-Hello\r\n".encode())

# Salutations upon greetings recieval
if(ta.recv(10000).decode() == "Admin-Greetings\r\n"):
    ta.sendall("Who\r\n".encode())
    print("The players currently playing are: ")
    while currentPlayers != "":
        currentPlayers = ta.recv(10000).decode()
        print(currentPlayers)
    
    
    

