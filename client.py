#!/usr/bin/python3           # This is client.py file
import socket
import json

class Client:

    def __init__(self,host,port,type):
        self.host = host
        self.port = port
        self.BUFFER_SIZE = 1024
        self.client_type = type

    def establish_connection(self):
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((self.host, self.port))
        while(True):
            prompt = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(prompt)

            verb = input("Action: ")
            if(verb == "EXIT" or verb == ''):
                conn_socket.close()
                break
            code = input("Code: ")
            if(verb == "write" or verb == "update"):
                state = input("State: ")
                time = input("Time: ")
                package = {"verb": verb, "code":code,
                           "state":state, "time":time ,
                           "client_type":self.client_type}
            else:
                package = {"verb": verb , "code":code ,
                       "client_type":self.client_type}

            conn_socket.sendall(json.dumps(package).encode('utf-8'))

            response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(f"{str(response)}")

def main():
    #client = Client(socket.gethostname(),9999,"reader")
    client = Client(socket.gethostname(),9999,"writer")
    client.establish_connection()


if __name__ == "__main__":
    main()
