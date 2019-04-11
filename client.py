#!/usr/bin/python3           # This is client.py file
import socket

class Client:

    def __init__(self,host,port):
        self.host = host;
        self.port = port;
        self.BUFFER_SIZE = 1024

    def establish_connection(self):
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((self.host, self.port))
        while(True):
            response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(response)
            message = input("Message : ")
            if(message == "EXIT" or message == ''):
                conn_socket.close()
                break
            conn_socket.sendall(message.encode('utf-8'))
            response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(f"{str(response)}")

def main():
    client = Client(socket.gethostname(),9999)
    client.establish_connection()


if __name__ == "__main__":
    main()
