import asyncio
from threading import Thread


class ConnectTo(Thread):
    def __init__(self, host, port, label):
        Thread.__init__(self)
        self.label = label
        self.writer = None
        # get the content of the text field
        self.content = self.label.get("1.0", "end")
        self.host = host
        self.port = port
        self.connected = False

    async def tcp_echo_client(self, host, port):
        reader, writer = await asyncio.open_connection(host, port)
        self.connected = True
        self.writer = writer
        self.send_msg("a")
        # thread = Thread(target=self.send_msg, args=(writer,))
        # thread.start()
        while True:
            data = await reader.read(9999999)
            recived_message = data.decode()
            if recived_message:
                self.label.delete(1.0, "end")
                self.label.insert(1.0, recived_message)

    # called when textarea
    def send_msg(self, new_content):
        self.writer.write(new_content.encode())

    def run(self):
        asyncio.run(self.tcp_echo_client(self.host, self.port))

