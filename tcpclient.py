from socket import *
import argparse
import random
def main():
    parser = argparse.ArgumentParser(description="TCP 客户端")
    parser.add_argument("Lmin", type=int, help="数据块长度的最小值")
    parser.add_argument("Lmax", type=int, help="数据块长度的最大值")
    parser.add_argument("server_ip", help="服务器的IP地址")
    parser.add_argument("server_port", type=int, help="服务器的端口号")
    args = parser.parse_args()
    server_ip = args.server_ip
    server_port = args.server_port
    buffer_sizes =[] 
    n=0
    Lmin=args.Lmin
    Lmax=args.Lmax
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server_ip, server_port))
    while True:
        buffer_sizes.append(random.randint(Lmin, Lmax))
        n+=1
        if(sum(buffer_sizes)>=3147):
            break
    Type=(1).to_bytes(2, byteorder='big') 
    Innitialization_message=Type+n.to_bytes(4, byteorder='big')
    clientSocket.send(Innitialization_message)
    # 连接服务器

    output_file_content = []
    reversed_message = clientSocket.recv(2)
    Type=int.from_bytes(reversed_message, byteorder='big') 
    if(Type==2):      
        # 打开输入文件
        with open('ASCII.txt', 'r') as file:
            for i in range(n):
                # 读取文件中的一块
                block = file.read(buffer_sizes[i])
                if not block:
                    break
                # 发送块到服务器
                Type=(3).to_bytes(2, byteorder='big') 
                lenth=buffer_sizes[i].to_bytes(4, byteorder='big')
                message=Type+lenth+block.encode() 
                clientSocket.send(message)
                # 接收反转的文本块
                reversed_block = clientSocket.recv(1024)
                reversed_sentence=reversed_block[6:].decode()
                output_file_content.insert(0, reversed_sentence)
                print(f"{i+1}: {reversed_sentence}")
        # 将接收到的反转文本写入输出文件
        with open('reversed.txt', 'w') as output_file:
            output_file.write(''.join(output_file_content))

        print("客户端已完成，反转后的文件保存为 'reversed.txt'")
    else:
        print("服务端不同意连接")
    #关闭连接
    clientSocket.close()
if __name__ == "__main__":
    main()
