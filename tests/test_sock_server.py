from json import loads
from threading import Thread
from event_emiter import SocketServer, FileReader

server = SocketServer()

@server.on("connection")
def handle_new_connection(client, addr):
    print(f"[{addr[0]}:{addr[1]}] - CONNECTED")

@server.on("listening")
def handle_listening(host, port):
    print(f"[LISTENING] server is running on {host}:{port}")

@server.on("message")
def handle_messages(client, addr, message):
    message = loads(message)
    events = message.keys()
    for event in events:
        server.emit(event, client, addr, message[event])

@server.on("disconnect")
def handle_disconnections(client, addr):
    print(f"[{addr[0]}:{addr[1]}] - DISCONNECTED")

@server.on("file-request")
def handle_file_request(client, addr, file_request_json):
    Thread(target=initiate_file_reader, args=(client, file_request_json.get("file_name"),)).start()

def initiate_file_reader(client, file_name=None):
    file_reader = FileReader(file_name)

    @file_reader.on("chunk")
    def handle_chunks(n_chunk, data):
        client.send(data)

    @file_reader.on("end")
    def handle_end():
        client.send("completed".encode())

    file_reader.init()


server.start_server()
