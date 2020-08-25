from StatusCodes import status_codes
from TcpServer import TcpServer
from HttpRequest import HttpRequest
import mimetypes
import os

class HttpServer(TcpServer):
    """
        Constants
    """
    headers = {
        'Server': 'HttpServer',
        'Content-Type': 'text/html; charset=UTF-8',
        'Cache-Control': 'public'
    }
    blank_line = "\r\n".encode('utf-8')


    """
        @Override
        Handler override for TCP Server
    """
    def handle_request(self, data):
        request = HttpRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)

        return response


    """
        HTTP Request Method Handlers
    """
    def handle_OPTIONS(self, request):
        response_line = self.response_line(status_code=200)

        response_headers = self.response_headers({
            "Allow": "OPTIONS, GET"
        })

        response = (
            response_line,
            response_headers,
            self.blank_line
        )

        return "".join(response).encode('utf-8')

    def handle_GET(self, request):
        filename = request.uri.strip('/')
        if filename == '':
            filename = 'index.html'

        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                response_body = f.read()
                
            response_line = self.response_line(status_code=200)

            content_type = mimetypes.guess_type(filename)[0] or "text/html"
            response_headers = self.response_headers({
                "Content-Type": content_type,
                "Set-Cookie": "username=admin"
            })
        else:
            response_body = "<h1>404 Not Found</h1>"
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()

        response = (
            response_line,
            response_headers,
            self.blank_line,
            response_body
        )

        return b''.join(response)

    def handle_POST(self, request):
        response_line = self.response_line(status_code=200)
        response_headers = self.response_headers()

        response = (
            response_line,
            response_headers,
            self.blank_line,
            "Posted data to database!"
        )

        return b''.join(response).encode('utf-8')

    def handle_PUT(self, request):
        pass

    def handle_DELETE(self, request):
        pass

    def HTTP_501_handler(self, request):
        response_body = "<h1>501 Not Implemented<h1>"
        response_line = self.response_headers(status_code=501)
        response_headers = self.response_headers()

        response = (
            response_line,
            response_headers,
            self.blank_line,
            response_body
        )

        return b''.join(response).encode('utf-8')


    """
        Helper methods
    """
    def response_line(self, status_code):
        reason = status_codes[status_code][0]
        response_line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)
        return response_line.encode('utf-8')

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for header in headers_copy.keys():
            headers += "%s: %s\r\n" % (header, headers_copy[header])

        return headers.encode('utf-8')
