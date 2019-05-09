#!/usr/bin/python3
import socket
import json
import random
import threading
import sys

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
        try:
            conn_socket.connect((self.host, self.port))
        except socket.error as e:
            sys.exit("""
                    [+] Server is Unavailabe
                    [+] Exiting ...
                    """)

        #receive prompt
        prompt = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(prompt)
        while(True):
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
    if len(sys.argv) != 2:
        print("""
              [+] Run client program with one argument.
              [+] The argument indicates the client's type
              [+] e.g python client.py writer
              [+]     python client.py reader
              """)
    elif (sys.argv[1] == 'reader' or sys.argv[1] == 'writer'):
        Client(sys.argv[1]).establish_connection()

if __name__ == "__main__":
    main()
