import socket
from _thread import *
import os

server_dir = "server_files"

def recv_all(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Соединение разорвано")
        data += chunk
    return data

def com_list(con):
    files = os.listdir(server_dir)
    if files:
        answer = "\n".join(files)
    else:
        answer = "Нет файлов"
    con.send(answer.encode())

def com_download(con, filename):
    if not filename:
        con.send("Имя файла не указано".encode())
        return

    filepath = os.path.join(server_dir, os.path.basename(filename))
    if not os.path.exists(filepath):
        con.send("Файл не найден".encode())
        return

    file_size = os.path.getsize(filepath)
    con.send(str(file_size).encode())
    con.send("Y/N?".encode())

    confirm = con.recv(1024).decode()
    if confirm == "Y":
        with open(filepath, "rb") as f:
            con.sendall(f.read())
        print(f"[DOWNLOAD] {filename} ({file_size} байт)")
    else: return

def com_upload(con, filename):
    size_data = con.recv(1024).decode()
    file_size = int(size_data)
    print("получен размер файла: ", file_size)
    con.send("Y".encode())

    file_data = recv_all(con, file_size)
    filepath = os.path.join(server_dir, os.path.basename(filename))
    with open(filepath, "wb") as f:
        f.write(file_data)
    con.send("Файл загружен".encode())


def client_thread(con):
    print("connection: ", con)
    con.send("Hello, Client!".encode())
    while True:
        data = con.recv(1024)
        if not data:
            break

        message = data.decode().strip()
        parts = message.split(" ", 1)
        command = parts[0].upper()
        argument = parts[1] if len(parts) > 1 else ""

        if command == "EXIT":
            con.send("Bye, Client!".encode())
            con.close()
            break
        elif command == "LIST":
            com_list(con)
        elif command == "DOWNLOAD":
            com_download(con, argument)
        elif command == "UPLOAD":
            com_upload(con, argument)
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