from HttpServer import HttpServer

if __name__ == "__main__":
    server = HttpServer(bind_ip="192.168.1.167")
    server.start()