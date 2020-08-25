class HttpRequest:
    def __init__(self, data):
        self.method = None
        self.uri = '/'
        self.http_version = '1.1'
        self.headers = {}

        self.parse(data)

    def parse(self, data):
        data_decoded = data.decode('utf-8')
        lines = data_decoded.split("\r\n")
        request_line = lines[0]
        self.parse_request_line(request_line)

    def parse_request_line(self, request_line):
        request_words = request_line.split(' ')
        self.method = request_words[0]

        if len(request_words) > 1:
            self.uri = request_words[1]

        if len(request_words) > 2:
            self.http_version = request_words[2]
