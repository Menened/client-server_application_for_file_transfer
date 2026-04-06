import socket
import os

client = socket.socket()
hostname = socket.gethostname()
port = 12345
client.connect((hostname, port))
data = client.recv(1024)
print("server:",data.decode())

def recv_all(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Соединение разорвано")
        data += chunk
    return data


def com_download(client, filename):
    client.send(f"DOWNLOAD {filename}".encode())

    ans = client.recv(1024).decode()
    try:
        file_size = int(ans)
    except ValueError:
        print("server: ", ans)
        return
    ans = client.recv(1024).decode()
    print("server: ", ans)
    message =  (input())
    client.send(message.encode())
    if message == "Y":
            file_data = recv_all(client, file_size)
            save_path = os.path.basename(argument)
            with open(save_path, "wb") as f:
                f.write(file_data)

            print(f"Файл {save_path} сохранен ({file_size} байт)")



def com_upload(client, filename):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return
    file_size = os.path.getsize(filename)
    if file_size == 0:
        print("Файл пустой")
        return
    
    client.send(f"UPLOAD {filename}".encode())
    client.send(str(file_size).encode())
    ans = client.recv(1024).decode()
    if ans != "Y":
        print("server: ", ans)
        return
    with open(filename, "rb") as f:
        client.sendall(f.read())
    
    result = client.recv(1024).decode()
    print("server: ", result)



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
        com_download(client, argument)
    elif command == "UPLOAD":
        com_upload(client, argument)
        
    else:
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())

print("client shutdown")
client.close()
