import socket

client = socket.socket()
hostname = socket.gethostname()
port = 12345
client.connect((hostname, port))
data = client.recv(1024)
print("server:",data.decode())


while True:
    message = (input("Input a command: "))
    if message == "EXIT":
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())
        break
    elif message == "LIST":
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())
    else:
        client.send(message.encode())
        data = client.recv(1024)
        print("server: ", data.decode())
print("client shutdown")
client.close()
