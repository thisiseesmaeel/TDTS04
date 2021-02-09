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
    
    while True: # Server is runing all the time
        serverSideSocket, addr = welcomeSocket.accept()
        
        message = handle_client(serverSideSocket) # handles clients request and alters it if needed
        
        if len(message) != 0:
            destinationPort, destinationIP = port_and_ip(message)
            
            clientSideSocket = socket(AF_INET, SOCK_STREAM)
            clientSideSocket.connect((destinationIP, destinationPort))
            clientSideSocket.send(message.encode("utf-8"))

            responseMessage = clientSideSocket.recv(1024)
            is_text = is_text_content(responseMessage.decode("utf-8", "ignore")) # Checks if response content is text
            while True:
                if len(responseMessage) != 0:
                    if is_text: # if content is text then alter it
                        alteredMessage = alter_response(responseMessage.decode("utf-8", "ignore"))
                        serverSideSocket.send(alteredMessage.encode("utf-8"))
                    else: # if not text (image) send in directly to the browser
                        serverSideSocket.send(responseMessage)
                else:
                    serverSideSocket.close()
                    break
                responseMessage = clientSideSocket.recv(1024)
                
            clientSideSocket.close()

            
def handle_client(serverSideSocket):
    message = serverSideSocket.recv(1024).decode("utf-8", "ignore")
    altered_message = alter_message(message)
    
    return altered_message

def port_and_ip(message):
    match = re.search(r"Host: (.+[a-z])(:\d+)?", message)
    ip = match.group(1)
    
    if match.group(2): #ex: 127.0.0.2:400 which means this request should be send to port 400
        port = int(match.group(2)[1:])
    else: #otherwise the port for http must be used
        port = 80
            
    return port, ip
        
def alter_message(strContent):
    alteredContent = re.sub("smiley", "trolly", strContent)
        
    return alteredContent
    
def alter_response(strContent):
    alteredContent = re.sub("Smiley", "Trolly", strContent)
    alteredContent = re.sub("Stockholm", "Linköping", alteredContent)
    alteredContent = re.sub("/Linköping", "/Stockholm", alteredContent) #changes /Linköping back to /Stockholm due Linköping-image does not exist
   
    return alteredContent

def is_text_content(strContent):
    if re.search("Content-Type: text", strContent):
        return True
    return False


if __name__ == "__main__":
    start()
