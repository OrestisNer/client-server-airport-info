#!/usr/bin/python3           # This is server.py file
import socket

class Server:

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.BUFFER_SIZE = 1024

    def start(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind to the port
        serversocket.bind((self.host, self.port))
        # queue up to 5 requests
        serversocket.listen(5)

        while True:
           # establish a connection
           clientsocket,addr = serversocket.accept()
           #clientsocket.send(self.show_prompt().encode('utf-8'))
           print("Got a connection from %s" % str(addr))
           client_message = clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')
           print(client_message)
           server_response = "From server: "+client_message
           clientsocket.send(server_response.encode('utf-8'))
           clientsocket.close()

    def show_prompt(self):
        return """
                1 - Εισαγωγή
                2 - Διαγραφή
                3 - Τροποποίηση
                """

def main():
    server = Server(socket.gethostname(),9999)
    server.start()


if __name__ == "__main__":
    main()
