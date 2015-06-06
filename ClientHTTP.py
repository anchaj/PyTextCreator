import httplib


class ClientHTTP(object):
    """
    Simple http client, which can download data via POST, GET and HEAD
    """
    def __init__(self, address, port=httplib.HTTP_PORT):
        """
        Function initialize http client parameters, like address and port
        :param address: address to send post
        :param port: http port - default 80
        """
        self.address = address
        self.port = port

    def execute_post(self, path="", parameter_list={}):
        """
        This function executing POST on server, and return response data
        :param path: path to send post
        :param parameter_list: dictionary of post params
        :return: response data in string
        """
        http_client = httplib.HTTPConnection(self.address, self.port)

        try:
            http_client.request("POST", path, self.prepare_data(parameter_list))
            response = http_client.getresponse()
            return response.read()
        except httplib.HTTPException:
            print("Execute post exception")
        finally:
            if http_client is not None:
                http_client.close()

    def execute_get(self, path=""):
        """
        This function executing GET on server, and return response data
        :param path: path to send GET
        :return: response data in string
        """
        http_client = httplib.HTTPConnection(self.address, self.port)
        try:
            http_client.request("GET", path)
            response = http_client.getresponse()
            return response.read()
        except httplib.HTTPException:
            print("Execute get exception")
        finally:
            if http_client is not None:
                http_client.close()

    def execute_head(self, path=""):
        """
        This function executing HEAD on server, and return response data
        :param path: path to send HEAD request
        :return: response data in string
        """
        http_client = httplib.HTTPConnection(self.address, self.port)
        try:
            http_client.request("HEAD", path)
            response = http_client.getresponse()
            return response.read()
        except httplib.HTTPException:
            print("Execute get exception")
        finally:
            if http_client is not None:
                http_client.close()

    @staticmethod
    def prepare_data(data={}):
        """
        Function create param string from dictionary
        :param data: dictionary of parameters
        :return: parsed string of parameters
        """
        string = ""
        for i, j in data.iteritems():
            string += "&" + i + "=" + j
        if len(string) != 0:
            string = string[1:]
        return string

