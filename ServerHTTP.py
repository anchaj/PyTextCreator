import BaseHTTPServer
from cgi import parse_header, parse_multipart
from urlparse import parse_qs

HOST_NAME = "localhost"
PORT = 1050


class ServerHTTP(object):
    """
    Implementation of BaseHTTPServer, this class allow to start and shutdown serwer in any time.
    """
    def __init__(self, host=HOST_NAME, port=PORT, handler_on_post_callable=None):
        """
        Method can initialize needed data for start server.
        :param host: host where server will be running
        :param port: post wchich server will be using
        :param handler_on_post_callable: this field can be method or callable object. This 'field' is called
        after post request for create response for post. Have one param and it is a data returned from __parse_post
        method. handler_on_post_callable return created post response.
        :return: Nothing
        """
        def handler(*args):
            """
            Simple function need for create Handler class with not default constructor
            :param args: rest of argument for Handler constructor
            :return: Nothing
            """
            Handler(handler_on_post_callable, *args)

        self.__handler = handler
        ser_class = BaseHTTPServer.HTTPServer
        self.__server = ser_class((host, port), self.__handler)

    def close(self):
        """
        Method can close server.
        :return: Nothing
        """
        self.__server.server_close()

    def start(self):
        """
        Method can start server.
        :return: Nothing
        """
        try:
            self.__server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

    def get_handler_instance(self):
        """
        Method can be used for get instance of server handler
        :return: instance of handler
        """
        return self.__handler


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, sth_callable, *args):
        """
        Initialization method of Handler, this method run constructor of base handler class.
        :param sth: it is something callable used after post request for creating post response
        :param args: rest of constructor arguments for create base handler class
        :return: Nothing
        """
        self.__post_data = {}
        self.__on_post_call = sth_callable
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args)

    def do_HEAD(self):
        """
        Method used after HEAD request. Send headers to HTTP client.
        :return: Nothing
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """
        Method used after GET request. Send header and website context to HTTP client.
        :return:
        """
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
        """
        Method used after POST request. Send headers and response for POST request to HTTP client.
        :return:
        """
        try:
            self.__post_data = self.__parse_post()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if self.__on_post_call is not None:
                data = self.__on_post_call(self.__post_data)
                self.wfile.write(data)

        except RuntimeError:
            print("Post runtime exception")

    def __parse_post(self):
        """
        Method is used after post response, creating dictionary from POST data.
        :return: Dictionary of POST-ed data
        """
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
