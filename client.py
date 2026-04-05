import socket
import os

client = socket.socket()
hostname = socket.gethostname()
port = 12345
client.connect((hostname, port))
data = client.recv(1024)
print("server:",data.decode())

def recv_all(sock, size):
    """Получить ровно size байт."""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Соединение разорвано")
        data += chunk
    return data

while True:
    message = (input("Input a command: "))

    parts = message.split(" ", 1)
    command = parts[0].upper()
    argument = parts[1] if len(parts) > 1 else ""

    if command == "EXIT":
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())
        break
    elif command == "LIST":
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())
    elif command == "DOWNLOAD":
        client.send(message.encode())
        data = client.recv(1024)
        filesize = int(data.decode())
        print("server: ", data.decode())
        data = client.recv(1024)
        print("server: ", data.decode())
        message = (input())
        client.send(message.encode())
        if message == "Y":
            file_data = recv_all(client, filesize)
            save_path = os.path.basename(argument)
            with open(save_path, "wb") as f:
                f.write(file_data)

            print(f"Файл {save_path} сохранен ({filesize} байт)")
    # elif command == "UPLOAD": 
        
        
    else:
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())

print("client shutdown")
client.close()
