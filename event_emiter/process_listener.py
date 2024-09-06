from .event_emiter import EventEmitter
from subprocess import Popen, PIPE
from threading import Thread

class Process(EventEmitter):
    pid: int
    name: str | None

    def __init__(self, process, name=None):
        super().__init__()
        self.name = name
        self.process = Popen(process, stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True, bufsize=1)
        self.pid = self.process.pid
        Thread(target=self._monitor_output, daemon=True).start()
        Thread(target=self._monitor_error, daemon=True).start()

    def _monitor_output(self):
        for line in self.process.stdout.readlines():
            self.emit('output', line.strip(), self.pid, self.name)
        self.process.stdout.close()

    def _monitor_error(self):
        for line in self.process.stderr.readlines():
            self.emit('error', line.strip(), self.pid, self.name)
        self.process.stderr.close()

    def send_input(self, input_data):
        self.process.stdin.write(input_data + '\n')
        self.process.wait()

    def start_process(self):
        self.process.wait()

    def kill(self):
        self.process.kill()

    def close(self):
        self.process.terminate()
        self.process.wait()
