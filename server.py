import socket

server = socket.socket()
hostname = socket.gethostname()
port = 12345
server.bind((hostname, port))
server.listen(2)

print("server running...")
con, addr = server.accept()

print("connection: ", con)
print("client address: ", addr)

greet = "Hello Client!"
con.send(greet.encode())
con.close()

print("shutdown")
server.close()