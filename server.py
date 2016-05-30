# THINGS YET TO IMPLEMENT
# Error checking Try/Catch/Continue
# Score

#Server TCP
# TCP due to connection orentated protocol, highly reliable, data remains intact, does error checking
import socket
import random
import re
import select
import ssl

# Create server socket (socket.AF_INET = constant values family of protocols used as transport mechanism, socket.SOCK_STREAM = type of communications between end points)
l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l.bind(("127.0.0.1", 4000)) # Bind socket to specific address and port for communication

a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a.bind(("127.0.0.1", 4001)) # Bind socket to specific address and port for communication

# Asynchronous server implementation
socks = [] # list all of active sockets
socks.append(l)
socks.append(a)

# Global Variables
guessNumber = ""
randomNumber = 0
iRandom = 0
number = 0
randomDict = {}
ip = {}

# Proximity function
def within(value, goal, n):
    numDifference = abs(value - goal)
    if (numDifference <= n):
        return True
    else:
        return False
 
l.listen(5) # tell operating system to start listening for new connections
a.listen(1)               

# Connection open loop
while True:
    (sockIn, sockOut, err) = select.select(socks, [], [])
    
    #process all sockets with input
    for i in sockIn:
        if(i == l):
            (s,ca)=l.accept()#Establish connection with client (s = socket object, ca = Network address and client connection port)

            socks.append(s)
            
            # Dictionary assigns random number to connection
            randomDict[s] = random.randrange(0, 21)

            ip[s] = ca
            
            #Greeting Exchange
            greetingType = s.recv(10000).decode()
            if(greetingType == "Hello\r\n"):
                s.sendall("Greetings\r\n".encode())
            else:
                    s.sendall("A formatting error has occured your connection has been closed\r\n".encode())
                    socks.remove(i)
                    del randomDict[i]
                    del ip[i]
                    i.close()
        elif(i == a):
            (s,ca)=a.accept()
            # SSL
            ts = ssl.wrap_socket(s, certfile="5cc515_server.crt", keyfile="5cc515_server.key",
            server_side=True, cert_reqs=ssl.CERT_REQUIRED, ca_certs="5cc515-root-ca.cer")
            socks.append(ts)

            if(ts.recv(10000).decode()== "Admin-Hello\r\n"):
                ts.sendall("Admin-Greetings\r\n".encode())
                if(ts.recv(10000).decode()== "Who\r\n"):
                    for key in ip:
                        ts.sendall((str(ip[key]) + "\r\n").encode())                       
        else:
            try:
                iRandom = randomDict[i]
                # Recieve Guess#
                guessNumber = i.recv(10000).decode()
                # Seperate string from number
                number = re.search(r'\d+', guessNumber).group()
                number = int(number)

                if(within(number,iRandom , 0)):
                    i.sendall("Correct\r\n".encode())
                    socks.remove(i)
                    del randomDict[i]
                    del ip[i]
                    i.close()
                elif (within(number, iRandom, 2)):
                    i.sendall("Close\r\n".encode())
                else:
                    i.sendall("Far\r\n".encode())
            except:
                socks.remove(i)
                i.close()
        



