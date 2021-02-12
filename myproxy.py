from socket import *
import re
import zlib
import gzip

PROXY_PORT = 12000
PROXY_NAME = gethostbyname(gethostname()) # Which in my case is: "127.0.1.1"

welcomeSocket = socket(AF_INET,SOCK_STREAM)
welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Frees the port after force-stopping the proxy
welcomeSocket.bind((PROXY_NAME, PROXY_PORT))
welcomeSocket.listen(1)
print('The server is ready to receive...\n{0}'.format("="*40))
    
while True:
    serverSocket, addr = welcomeSocket.accept()
    print("{} connected to the Server!\n".format(addr))
    
    message = serverSocket.recv(1024).decode("utf-8", "ignore")
    
    if len(message) > 0:
        m = re.search(r"Host: (.+[a-z])(:\d+)?", message)
        host = m.group(1)
        # if m.group(2):
        #     port = int(m.group(2)[1:])
        # else:
        #     port = 80
        port = 80
        print("Port is:\t {0}\nHost is:\t{1}\nLength of hostname is:\t{2}\n\nMessage is:\n{3}"
              .format(port, host, len(host), message))
            
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((host, port))
        clientSocket.send(message.encode("utf-8"))

        chunk = clientSocket.recv(1024)

        m = re.search(r"Content-Length: (\d+)", chunk.decode("utf-8", "ignore"))
        size = int(m.group(1))
        
        recv = len(chunk)
        
        first = True
        full_msg = b""
        while True:
           
            if recv >= size:
                
                #serverSocket.close()
                print("Bye")
                break
            else:
                
                if first:
                    first = False
                    print(chunk.decode("utf-8", "ignore"))
                #full_msg += chunk
                # chunk = gzip.decompress(chunk)
                # chunk = gzip.compress(chunk)
                serverSocket.sendall(chunk)
                #print("Response is:\n\n{0}\n\n".format(chunk.decode("utf-8", "ignore")))
                
            chunk = clientSocket.recv(1024)
            #print(type(chunk))
            print (len(chunk))
            recv += len(chunk)
            print ("recv bytes is: ", recv)

    serverSocket.close()
            
