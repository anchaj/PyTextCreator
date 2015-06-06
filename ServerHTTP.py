import BaseHTTPServer
from cgi import parse_header, parse_multipart
from urlparse import parse_qs

HOST_NAME = "localhost"
PORT = 1050



class ServerHTTP(object):
    def __init__(self, host=HOST_NAME, port=PORT, handler_on_post_callable=None):
        def handler(*args):
            Handler(handler_on_post_callable, *args)

        self.__handler = handler
        ser_class = BaseHTTPServer.HTTPServer
        self.__server = ser_class((host, port), self.__handler)

    def close(self):
        self.__server.server_close()

    def start(self):
        try:
            self.__server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

    def get_handler_instance(self):
        return self.__handler


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, sth, *args):
        self.__post_data = {}
        self.__on_post_call = sth
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        try:
            with open("index.html") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(data)
        except IOError:
            self.send_response(404)

    def do_POST(self):
        try:
            self.__post_data = self.parse_post()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if self.__on_post_call is not None:
                data = self.__on_post_call(self.__post_data)
                self.wfile.write(data)

        except RuntimeError:
            print("Post runtime exception")

    def parse_post(self):
        content_type, parse_dictionary = parse_header(self.headers['Content-type'])
        if content_type == 'multipart/form-data':
            post_variables = parse_multipart(self.rfile, parse_dictionary)
        elif content_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            post_variables = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            post_variables = {}
        return post_variables

    def get_post_data(self):
        return self.__post_data
