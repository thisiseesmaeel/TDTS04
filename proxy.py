from socket import *
import re

PROXY_PORT = 12000
PROXY_NAME = gethostbyname(gethostname()) # Which in my case is: "127.0.1.1"

def start():
    welcomeSocket = socket(AF_INET,SOCK_STREAM)
    welcomeSocket.bind((PROXY_NAME, PROXY_PORT))
    welcomeSocket.listen(1)
    print('The server is ready to receive...\n{0}\n'.format("="*40))
    
    while True:
        serverSideSocket, addr = welcomeSocket.accept()
        message = serverSideSocket.recv(1024)
        
        if len(message) != 0:
            match = re.search(r"Host: (.+[a-z])(:\d+)?", message.decode("utf-8"))
            destinationIP = match.group(1)
            if match.group(2):
                destinationPort = int(match.group(2)[1:])
            else:
                destinationPort = 80
                
            print("Port is:\t {0}".format(destinationPort))
            print("Host is:\t{}\nLength of hostname is:\t{}\nMessage is:\n{}".format(destinationIP, len(destinationIP), message.decode("utf-8")))
            #capitalizedMessage = message.upper()

            clientSideSocket = socket(AF_INET, SOCK_STREAM)
            clientSideSocket.connect((destinationIP, destinationPort))
            clientSideSocket.send(message)
                       
            while True:
                responseMessage = clientSideSocket.recv(1024).decode("utf-8")
                if len(responseMessage) != 0:
                    alteredMessage = alter_message(responseMessage)
                    serverSideSocket.send(alteredMessage.encode("utf-8"))
                    print("Response is:\n\n{0}\nAltered message is:\n\n{1}\n{2}".format(responseMessage, alteredMessage, "="*40))
                else:
                    serverSideSocket.close()
                    break
            clientSideSocket.close()
           
        
def alter_message(msg):
    altered_msg = re.sub("Smiley", "Trolly", msg)
    altered_msg = re.sub("Stockholm", "Linköping", altered_msg)
    return altered_msg

if __name__ == "__main__":
    start()
