import socket
from _thread import *
import os

server_dir = "server_files"

def com_list(con):
    files = os.listdir(server_dir)
    if files:
        answer = "\n".join(files)
    else:
        answer = "No files"
    con.send(answer.encode())

def client_thread(con):
    print("connection: ", con)
    con.send("Hello, Client!".encode())
    while True:
        data = con.recv(1024)
        command = data.decode()
        if command == "EXIT":
            con.send("Bye, Client!".encode())
            con.close()
            break
        elif command == "LIST":
            com_list(con)
        else:
            con.send("Wrong command".encode())


server = socket.socket()
hostname = socket.gethostname()
port = 12345
server.bind((hostname, port))
server.listen(2)

print("server running...")
while True:
    client, _ = server.accept()
    start_new_thread(client_thread, (client, ))