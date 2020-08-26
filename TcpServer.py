import socket

class TcpServer:
    packet_size = 1024
    maximum_queued_conns = 5

    def __init__(self, bind_ip="127.0.0.1", bind_port=8000):
        self.bind_ip = bind_ip
        self.bind_port = bind_port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.bind_ip, self.bind_port))
        sock.listen(self.maximum_queued_conns)

        print("[+] Listening at", sock.getsockname())

        while True:
            conn, addr = sock.accept()
            print("[+] Connected by", addr)

            data = conn.recv(self.packet_size)
            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        return data