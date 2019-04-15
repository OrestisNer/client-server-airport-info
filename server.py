#!/usr/bin/python3           # This is server.py file
import socket
import threading
import json
import time

class Server:

    def __init__(self):
        self.host = socket.gethostname()
        self.port = 9999
        self.BUFFER_SIZE = 1024
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.airport_routes = dict()


    def start_server(self):
        while True:
           client_socket,addr = self.serversocket.accept()
           print("Got a connection from %s" % str(addr))
           threading.Thread(target=self.open_connetion, args=(client_socket,addr, )).start()

    def show_prompt(self):
        return """
                Route Actions:
                [+] write
                [+] read
                [+] update
                [+] delete
                [+] EXIT
                """

    def open_connetion(self,client_socket,addr):
        while(True):
            client_socket.send(self.show_prompt().encode('utf-8'))
            client_package_json = client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            if not client_package_json:
                print("Lost connection with %s" % str(addr))
                break
            server_response = self.handle_package(client_package_json)
            client_socket.send(server_response.encode('utf-8'))
            self.print_routes()

        client_socket.close()

    def handle_package(self,client_package_json):
        client_data = json.loads(client_package_json)
        verb = client_data["verb"]
        client_type = client_data["client_type"]
        code = client_data["code"]
        if(verb == "read"):
            return self.read_route(code)
        elif(client_type == "writer"):
            if(verb == "delete"):
                return self.delete_route(code)
            elif(verb == "write"):
                state = client_data["state"]
                time = client_data["time"]
                return self.write_route(code,state,time)
            elif(verb == "update"):
                state = client_data["state"]
                time = client_data["time"]
                return self.update_route(code, state, time)

        return "Unavailabe action."

    def write_route(self,code,state,time):
        self.airport_routes[code] = {"code":code, "state": state,
                                     "time": time, "lock": threading.Lock()}
        return """
                [+]WOK
                [+]Successfuly add route with code """+code

    def read_route(self,code):
        try:
            route_data = self.airport_routes[code]
            route_data["lock"].acquire()
            self.action_delay("read")
            route_data["lock"].release()
            return "[+] ROK "+code+" "+route_data["state"]+" "+route_data["time"]
        except:
            return "RERR"

    def delete_route(self,code):
        try:
            route_data = self.airport_routes[code]
            route_data["lock"].acquire()
            self.action_delay("delete")
            del self.airport_routes[code]
            route_data["lock"].release()
            return "[+] ROK Route with code "+code+" successfuly deleted"
        except:
            return "RERR"

    def update_route(self,code,state,time):
        try:
            route_data = self.airport_routes[code]
            route_data["lock"].acquire()
            self.action_delay("update")
            if state :
                route_data["state"] = state

            if time :
                route_data["time"] = time
            route_data["lock"].release()
            return "[+] ROK Route with code "+code+" successfuly updated"
        except:
            return "RERR"


    def action_delay(self,verb):
        if verb == "read":
            time.sleep(2)
        else:
            time.sleep(5)


    def print_routes(self):
        for i in self.airport_routes:
            print(self.airport_routes[i]["code"] + "|" +
                  self.airport_routes[i]["state"]+ "|" +
                  self.airport_routes[i]["time"] + "|")

if __name__ == "__main__":
    Server().start_server()
