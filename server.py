#!/usr/bin/python3           # This is server.py file
import socket
import threading
import json

class Server:

    def __init__(self):
        self.host = socket.gethostname()
        self.port = 9999
        self.BUFFER_SIZE = 1024
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.airport_data = dict()


    def start(self):
        while True:
           client_socket,addr = self.serversocket.accept()
           print("Got a connection from %s" % str(addr))
           threading.Thread(target=self.open_connetion, args=(client_socket, )).start()

    def show_prompt(self):
        return """
                1 - Εισαγωγή
                2 - Διαγραφή
                3 - Τροποποίηση
                """

    def open_connetion(self,client_socket):
        while(True):
            client_socket.send(self.show_prompt().encode('utf-8'))
            client_package_json = client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            if(client_package_json == "EXIT"):
                break

            server_response = self.handle_package(client_package_json)
            client_socket.send(server_response.encode('utf-8'))

        client_socket.close()

    def handle_package(self,client_package_json):
        client_data = json.loads(client_package_json)
        verb = client_data["verb"]
        client_type = client_data["client_type"]
        code = client_data["code"]
        if(verb == "read"):
            pass
        elif(client_type == "writer"):
            if(verb == "delete"):
                pass
            elif(verb == "write"):
                state = client_data["state"]
                time = client_data["time"]
                return self.write_data(code,state,time)
            elif(verb == "update"):
                pass

        return "Unavailabe action."
        #return client_type

    def write_data(self,code,state,time):
        #TODO place a semaphore lock into list

        self.airport_data["code"] = {"code":code, "state": state,
                                     "time": time, "lock": threading.Lock()}




if __name__ == "__main__":
    Server().start()
