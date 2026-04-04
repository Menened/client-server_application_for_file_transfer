import socket
from _thread import *

def client_thread(con):
    print("connection: ", con)
    greet = "Hello, Client!"
    farewell = "Bye, Client!" 
    Error = "Wrong command"
    con.send(greet.encode())
    while True:
        data = con.recv(1024)
        command = data.decode()
        if command == "EXIT":
            con.send(farewell.encode())
            con.close()
            break
        else:
            con.send(Error.encode())


server = socket.socket()
hostname = socket.gethostname()
port = 12345
server.bind((hostname, port))
server.listen(2)

print("server running...")
while True:
    client, _ = server.accept()
    start_new_thread(client_thread, (client, ))