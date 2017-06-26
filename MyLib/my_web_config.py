"""
Web server to get module configuration information
Originally based on example code found at this link:
https://lab.whitequark.org/notes/2016-10-20/controlling-a-gpio-through-an-esp8266-based-web-server/
With significant modifications and enhancements to work in the module
environment and to accept configuration information rather than just toggling
a GPIO pin.
"""


# Begin configuration
TITLE    = "Test Input"
# End configuration

import machine
import usocket


class WebConfig:
    """
    Implement a basic web server to allow configuration of
    a network-connected device from a browser.

    A timeout parameter determines how long the check() method waits
    for an initial connection. The default is None which waits
    forever. Once a connection is made from a browser, the timeout
    value is set to None and the server will not timeout. In this case the
    user must specifically end the configuration session by selecting
    that option on the web page displayed by the browser.

    The goal is to also pass in the module configuration parameters that are
    displayed and can be changed from the browser, but this is not
    yet implemented.

    Normally the programmer will instantiate the WebConfig class, and
    and then call the check() method in a loop as long as it returns
    True. When check() returns False it means a timeout occurred.
    """

    def __init__(self, timeout=None):
        """
        Start the web server.

        The timeout parameter determines how long the server will
        wait for an initial connection from a browser, in seconds.
        Default is to wait forever.
        """
        self.server = usocket.socket()
        self.server.bind(('0.0.0.0', 8080))
        self.server.settimeout(timeout)
        self.server.listen(1)
        print('Listening on port 8080')

    def check(self):
        """
        Wait for a connection from a browser.

        If a timeout occurs, return False.

        If a connection is made,
          - set the timeout to None (wait forever)
          - handle the browser request
          - close the socket and return True
        """
        try:
            (socket, sockaddr) = self.server.accept()
        except (KeyboardInterrupt, SystemExit):
            raise
        except OSError as e:
            if e.args[0] == 110:
                # If the error says no data was available
                print('Timeout')
                return False
            else:
                raise
        print("Received request from", sockaddr)
        self.server.settimeout(None)
        self.handle(socket)
        socket.close()
        return True

    def ok(self, socket, query):
        socket.write('HTTP/1.1 200 OK\r\n\r\n')
        socket.write('<!DOCTYPE html><html><title>'+TITLE+'</title><body>')
        socket.write('<form method="POST" action="/action?">')
        socket.write('<input type="text" name="ap">')
        socket.write('<input type="submit" value="Submit">')
        socket.write('</form></body></html>')

    def err(self, socket, code, message):
        print('Error:', code, message)
        socket.write("HTTP/1.1 "+code+" "+message+"\r\n\r\n")
        socket.write("<h1>"+message+"</h1>")

    def handle(self, socket):
        line = socket.readline()
        print(line)
        if line:
            (method, url, version) = line.split(b" ")
            print(method, url, version)
            if b"?" in url:
                (path, query) = url.split(b"?", 2)
            else:
                (path, query) = (url, b"")
            print(path, query)
        else:
            return
        while True:
            header = socket.readline()
            print(header)
            if header == b"":
                return
            if header == b"\r\n":
                break
        print('Handling it')
        if version != b"HTTP/1.0\r\n" and version != b"HTTP/1.1\r\n":
            self.err(socket, "505", "Version Not Supported")
        elif method == b"GET":
            if path == b"/":
                print('Calling ok for GET')
                self.ok(socket, query)
                print('returned from ok for GET')
            else:
                self.err(socket, "404", "Not Found")
        elif method == b"POST":
            if path == b"/action":
                print('Reading body of message')
                body = socket.recv(1024)
                print(body)
                print('Calling ok for POST')
                self.ok(socket, query)
                print('Returned from ok for POST')
            else:
                self.err(socket, "404", "Not Found")
        else:
            self.err(socket, "501", "Not Implemented")

intfc = WebConfig(timeout=60)
while intfc.check():
    print('Go again')
print('Done')
