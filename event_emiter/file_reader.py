from event_emiter import EventEmitter

class FileReader(EventEmitter):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def init(self):
        self.emit("reading")
        with open(self.file_name, "rb") as file:
            chunk = 1
            while True:
                data = file.read(1024)
                if not data:
                    self.emit("end")
                    break
                self.emit(f"chunk", chunk, data)
                chunk += 1
