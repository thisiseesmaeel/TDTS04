from socket import *
serverName = "zebroid.ida.liu.se"
print(len(serverName))
serverPort = 80
request = """GET /fakenews/test1.txt HTTP/1.1
Host: zebroid.ida.liu.se
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1

"""
print(request)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
#sentence = input('Input lowercase sentence:')
clientSocket.send(request.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode())
clientSocket.close()

# ip = gethostbyname("zebroid.ida.liu.se")
# print(ip)
