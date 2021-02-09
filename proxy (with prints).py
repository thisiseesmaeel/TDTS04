from socket import *
import re

PROXY_PORT = 12000
PROXY_NAME = gethostbyname(gethostname()) # Which in my case is: "127.0.1.1"

def start():
    welcomeSocket = socket(AF_INET,SOCK_STREAM)
    welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Frees the port after force-stopping the proxy
    welcomeSocket.bind((PROXY_NAME, PROXY_PORT))
    welcomeSocket.listen(1)
    print('The server is ready to receive...\n{0}'.format("="*40))
    
    while True:
        serverSideSocket, addr = welcomeSocket.accept()
        message = serverSideSocket.recv(512).decode("utf-8", "ignore")
        message = alter_message(message)
        
        if len(message) != 0:
            match = re.search(r"Host: (.+[a-z])(:\d+)?", message)
            destinationIP = match.group(1)
            if match.group(2):
                destinationPort = int(match.group(2)[1:])
            else:
                destinationPort = 80
                
            print("Port is:\t {0}\nHost is:\t{1}\nLength of hostname is:\t{2}\n\nMessage is:\n{3}"
                     # .format(destinationPort, destinationIP, len(destinationIP), message))

            clientSideSocket = socket(AF_INET, SOCK_STREAM)
            clientSideSocket.connect((destinationIP, destinationPort))
            clientSideSocket.send(message.encode("utf-8"))

            responseMessage = clientSideSocket.recv(512)
            is_text = is_text_content(responseMessage.decode("utf-8", "ignore"))
            while True:
                if len(responseMessage) != 0:
                    if is_text:
                        alteredMessage = alter_response(responseMessage.decode("utf-8", "ignore"))
                        serverSideSocket.send(alteredMessage.encode("utf-8"))
                        print("Response is:\n\n{0}\n\nAltered response is:\n\n{1}\n{2}"
                             # .format(responseMessage.decode("utf-8", "ignore"), alteredMessage, "="*40))
                    else:
                        serverSideSocket.send(responseMessage)
                        print("Response contains no text.\n{0}".format("="*40))
                else:
                    serverSideSocket.close()
                    break
                responseMessage = clientSideSocket.recv(512)
                
            clientSideSocket.close()
           
        
def alter_message(strContent):
    alteredContent = re.sub("smiley", "trolly", strContent)
        
    return alteredContent
    
def alter_response(strContent):
    alteredContent = re.sub("Smiley", "Trolly", strContent)
    alteredContent = re.sub("Stockholm", "Linköping", alteredContent)
    alteredContent = re.sub("/Linköping", "/Stockholm", alteredContent)
   
    return alteredContent

def is_text_content(strContent):
    if re.search("Content-Type: text", strContent):
        return True
    return False

if __name__ == "__main__":
    start()
