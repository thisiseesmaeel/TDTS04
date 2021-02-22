from socket import * #Import evrything from socket.
import re #Import Regex


PROXY_PORT = 12000 #Set the proxy port to "12000"
PROXY_NAME = gethostbyname(gethostname()) #Which in my case is: "127.0.1.1"

def start():
    #welcomeSocket to recive request to establish connection
    welcomeSocket = socket(AF_INET,SOCK_STREAM)#ipv4/tcp
    #Frees the port after force-stopping the proxy otherwise you should wait for a while
    welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Frees the port after force-stopping the proxy
    #Bind the socket and listen on it
    welcomeSocket.bind((PROXY_NAME, PROXY_PORT))
    welcomeSocket.listen(6) #Allow 6 requests at the same time
    print('The server is ready to receive...\n{0}'.format("="*40))
    
    while True: #The proxy is runing allways
        # accept the request and save info about socket in "serverSideSocket"
        serverSideSocket, addr = welcomeSocket.accept()  
        # handles clients request and alters it if needed
        message = handle_client(serverSideSocket)
        
        if len(message) != 0: #run this block if message is not empty
            #Find port and Ip for dest of the message
            destPort, destIP = port_and_ip(message)
            #Create client socket and connect it to dest server then send altred message
            clientSideSocket = socket(AF_INET, SOCK_STREAM)#ipv4/tcp
            clientSideSocket.connect((destIP, destPort))
            clientSideSocket.send(message.encode("utf-8"))
            # recive first chunk of data from the server
            responseMessage = clientSideSocket.recv(1024)
            # Checks if response content is text
            is_text = is_text_content(responseMessage.decode("utf-8", "ignore")) 

            while True: # while we can read data, we continue same process 
                if len(responseMessage) != 0:
                    if is_text: # if content is text then alter it and send it to the server
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
    #recive 1024 bytes and decode it
    message = serverSideSocket.recv(1024).decode("utf-8", "ignore")
    #Change smiley to trolly in case there is any occurence 
    altered_message = alter_message(message)
    
    return altered_message

def port_and_ip(message):
    match = re.search(r"Host: (.+[a-z])(:\d+)?", message, re.IGNORECASE)
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
    #If it finds "Content-Type: text" that means the content is text, return True
    if re.search("Content-Type: text", strContent,  re.IGNORECASE):
        return True
    return False


if __name__ == "__main__":
    start()
