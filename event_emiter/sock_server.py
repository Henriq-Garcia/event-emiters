from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread, Lock
from event_emiter import EventEmitter

class SocketServer(socket, EventEmitter):
    def __init__(self, port: int = 5050, decode: str = "utf-8", disconnect_message: str = "!DISCONNECT"):
        socket.__init__(self, AF_INET, SOCK_STREAM)
        EventEmitter.__init__(self)
        self._HOST = gethostbyname(gethostname())
        self._PORT = port
        self._DECODE = decode
        self._DISCONNECT_MESSAGE = disconnect_message
        self._lock = Lock()
        self._CONNECTIONS = dict()
        self.bind((self._HOST, self._PORT))

    def start_server(self):
        self.listen()
        self.emit("listening", self._HOST, self._PORT)
        Thread(target=self._receive_connections).start()

    def _receive_connections(self):
        while True:
            client, addr = self.accept()
            self.emit("connection", client, addr)
            Thread(target=self._default_messages_handler, args=(client, addr)).start()

    def _default_messages_handler(self, client: socket, addr):
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = data.decode(self._DECODE)
            if self._DISCONNECT_MESSAGE in message:
                self.emit("disconnect", client, addr)
                break
            self.emit("message", client, addr, message)

    def __repr__(self):
        return f'SocketServer(HOST="{self._HOST}:{self._PORT}", DECODE="{self._DECODE}", NUM_CONNECTIONS={len(self._CONNECTIONS)})'
