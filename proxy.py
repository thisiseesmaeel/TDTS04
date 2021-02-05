from socket import *
import re

DESTINATION_PORT = 80
serverPort = 12000
server = '127.0.1.1'
#print(gethostbyname(gethostname()))
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((server,serverPort))
serverSocket.listen(1)
print('The server is ready to receive...\n{0}\n'.format("="*40))

while True:
    connectionSocket, addr = serverSocket.accept()
    # print("Client socket: ", connectionSocket)
    # print("Client address: ", addr)
    sentence = connectionSocket.recv(1024).decode('unicode_escape')
    
    
    match = re.search(r"Host: (.+[a-z]+)", sentence)
    destinationIP = match.group(1)
    print("Host is:\t{0}\nLength of hostname is:\t{1}\n\nMessage is:\n{2}".format(destinationIP, len(destinationIP), sentence))
    #capitalizedSentence = sentence.upper()

    clientSideSocket = socket(AF_INET, SOCK_STREAM)
    clientSideSocket.connect((destinationIP, DESTINATION_PORT))
    clientSideSocket.send(sentence.encode())
    modifiedSentence = clientSideSocket.recv(1024)
    print("Response is:\t{0}\n{1}".format(modifiedSentence.decode('unicode_escape'), "="*40))
    connectionSocket.send(modifiedSentence)
    
    clientSideSocket.close()
    connectionSocket.close()
