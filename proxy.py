from socket import *
import re

def start():
    PROXY_PORT = 12000
    PROXY_NAME = "127.0.1.1"
    #print(gethostbyname(gethostname()))
    welcomeSocket = socket(AF_INET,SOCK_STREAM)
    welcomeSocket.bind((PROXY_NAME, PROXY_PORT))
    welcomeSocket.listen(1)
    print('The server is ready to receive...\n{0}\n'.format("="*40))
    
    while True:
        serverSideSocket, addr = welcomeSocket.accept()
        message = serverSideSocket.recv(1024).decode('unicode_escape')
        match = re.search(r"Host: (.+[a-z])(:\d+)?", message)
        destinationIP = match.group(1)
        if match.group(2):
            destinationPort = int(match.group(2)[1:])
        else:
            destinationPort = 80
        
        print("Port is:\t {0}".format(destinationPort))
        print("Host is:\t{0}\nLength of hostname is:\t{1}\n\nMessage is:\n\n{2}".format(destinationIP, len(destinationIP), message))
        #capitalizedMessage = message.upper()
        
        clientSideSocket = socket(AF_INET, SOCK_STREAM)
        clientSideSocket.connect((destinationIP, destinationPort))
        clientSideSocket.send(message.encode())
        responseMessage = clientSideSocket.recv(1024).decode('unicode_escape')
        print("Response is:\n\n{0}\n{1}".format(responseMessage, "="*40))
        alteredMessage = alter_message(responseMessage)
        serverSideSocket.send(alteredMessage.encode())
        
        clientSideSocket.close()
        serverSideSocket.close()
        
def alter_message(msg):
    altered_msg = re.sub("Smiley", "Trolly", msg)
    return altered_msg

if __name__ == "__main__":
    start()
