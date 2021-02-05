from socket import *
import re

DESTINATION_PORT = 80
serverPort = 12000
server = '127.0.1.1'
#print(gethostbyname(gethostname()))
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((server,serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    # print("Client socket: ", connectionSocket)
    # print("Client address: ", addr)
    sentence = connectionSocket.recv(1024).decode('unicode_escape')
    match = re.search(r"Host: (.+)", sentence)
    destinationIP = match.group(1)[0:-1]
    print(len(destinationIP))
    print(destinationIP)
    #capitalizedSentence = sentence.upper()
    

    clientSideSocket = socket(AF_INET, SOCK_STREAM)
    clientSideSocket.connect((destinationIP, DESTINATION_PORT))
    clientSideSocket.send(sentence.encode())
    
    modifiedSentence = clientSideSocket.recv(1024)
    clientSideSocket.close()
    print(modifiedSentence.decode('unicode_escape'))
    #print(sentence)
    #connectionSocket.send(capitalizedSentence.encode())
    #connectionSocket.send("Hello World!".encode())
    connectionSocket.close()
