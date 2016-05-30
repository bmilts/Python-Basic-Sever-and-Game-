# Client TCP
import socket
import ssl
import sys

# Initiate global variables
gameLoop = False
guess = ""
assessment = ""

# Create client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 # SSL
#ts = ssl.wrap_socket(s, certfile="100352212.crt", keyfile="100352212.key", ca_certs="5cc515-root-ca.cer")

# Connect socket to server

s.connect(("127.0.0.1", 4000))
   

# Greetings Exchange
s.sendall("Hello\r\n".encode())

# Salutations upon greetings recieval
if(s.recv(10000).decode() == "Greetings\r\n"):
        print("Welcome to the guess the number game! ")

        
# Game Loop
while (gameLoop != True):
    # Input and send guess
    try:
        guess = int(input("What is your guess? "))
    except ValueError:
        print("That was not a valid guess. Try again...")
        continue
    intGuess = ("Guess: %i\r\n" % (guess))
    try:
        s.sendall(intGuess.encode())
    # Assess result
        assessment = (s.recv(10000).decode())
    except:
        print("Cannot connect to server, closing the program.")
        sys.exit()
    
    if(assessment == "Correct\r\n"):
        print("You guessed correctly!")
        gameLoop = True
    elif(assessment == "Close\r\n"):
        print("You are getting close!")
    elif(assessment == "Far\r\n"):
        print("You are way off.")
    
    
s.close()   
