#!/usr/bin/python3
import socket
import json
import random

class Client:

    def __init__(self,type):
        self.host = socket.gethostname()
        self.port = 9999
        self.BUFFER_SIZE = 1024
        self.client_type = type

    def establish_connection(self):
        """Function to force connectio between client and server"""
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to server
        conn_socket.connect((self.host, self.port))
        while(True):
            #receive prompt
            prompt = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(prompt)

            verb = input("Action: ")
            if verb == "EXIT" or verb =="":
                conn_socket.close()
                break

            #save data into dictionary
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

            #send data as json string
            conn_socket.sendall(json.dumps(package).encode('utf-8'))

            #get response and print it
            response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(f"{str(response)}")

def main():
    coin = random.randint(1, 3)
    if(coin==1):
        print("I am Writer")
        Client("writer").establish_connection()
    else:
        print("I am Reader")
        Client("reader").establish_connection()


if __name__ == "__main__":
    main()
