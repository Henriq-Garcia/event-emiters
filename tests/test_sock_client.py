from json import dumps
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM

host = ("172.25.32.1", 5050)

client = socket(AF_INET, SOCK_STREAM)
client.connect(host)

# while True:
client.send(dumps({
    "file-request": {
        "file_name": "hello_world.txt"
    }
}).encode())

buffer_size = 1024
while True:
    part = client.recv(buffer_size).decode()
    if "completed" in part:
        break
    else:
        print(part)
    sleep(2)