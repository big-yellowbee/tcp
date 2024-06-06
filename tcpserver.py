import selectors
import socket
import time
def main():
    server_ip = "0.0.0.0"
    server_port = 12345
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((server_ip, server_port))
    serverSocket.listen(1)
    serverSocket.setblocking(False)  # 设置为非阻塞模式

    sel = selectors.DefaultSelector()
    sel.register(serverSocket, selectors.EVENT_READ, accept)

    print(f"服务器已启动，在 {server_ip}:{server_port} 上监听")

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, sel)

def accept(serverSocket, sel):
    connectionSocket, addr = serverSocket.accept()
    print(f"新连接：{addr}")
    connectionSocket.setblocking(False)  # 设置为非阻塞模式
    sel.register(connectionSocket, selectors.EVENT_READ, read)

def read(connectionSocket, sel):
    sentence = connectionSocket.recv(1024)
    Type = sentence[:2]
    Type = int.from_bytes(Type, byteorder='big')
    n = sentence[2:]
    n=int.from_bytes(n, byteorder='big')
    if Type == 1:
        Type = (2).to_bytes(2, byteorder='big') 
        connectionSocket.send(Type)
        for i in range(n):
            time.sleep(0.1)
            sentence = connectionSocket.recv(1024)
            Type = sentence[:2]
            Type = int.from_bytes(Type, byteorder='big')
            if Type == 3: 
                length = sentence[2:6]
                reversed_sentence = sentence[6:]
                reversed_sentence = reversed_sentence[::-1]  # 反转文本
                Type = (4).to_bytes(2, byteorder='big')
                message = Type + length + reversed_sentence
                connectionSocket.send(message)
   
    print(f"连接关闭：{connectionSocket.getpeername()}")
    sel.unregister(connectionSocket)
    connectionSocket.close()

if __name__ == "__main__":
    main()
