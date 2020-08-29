import asyncio
from threading import Thread


class HostTo(Thread):
    def __init__(self, port, label):
        Thread.__init__(self)
        self.label = label
        self.content = self.label.get("1.0", "end")
        self.host = "0.0.0.0"
        self.port = port
        self.connected=False

    async def main(self):
        server = await asyncio.start_server(self.handle_echo, self.host, 8888)

        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")
        self.connected=True
        async with server:
            await server.serve_forever()

    async def handle_echo(self, reader, writer):
        self.writer = writer
        while True:

            data = await reader.read(9999999)
            message = data.decode()
            print(message)
            if message != self.content:
                self.label.delete(1.0, "end")
                self.label.insert(1.0, message)
                self.content = message

    def send_msg(self, new_content):
        self.writer.write(new_content.encode())

    # def write_msg(self,new_contetnt):
    #     while True:
    #         new_content = self.label.get("1.0", "end")
    #         if new_content != self.content:
    #             writer.write(new_content.encode())
    #             # await writer.drain()
    #             self.content = new_content

    def run(self):
        asyncio.run(self.main())

