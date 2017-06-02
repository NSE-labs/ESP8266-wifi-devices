"""
Experimental web server to get module configuration information
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
import micropython

micropython.alloc_emergency_exception_buf(100)

class WebConfig:
    def __init__(self):
        server = usocket.socket()
        server.bind(('0.0.0.0', 8080))
        server.listen(1)
        print('Listening on port 8080')
        while True:
            try:
                (socket, sockaddr) = server.accept()
                print("Received request from", sockaddr)
                self.handle(socket)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print('Exception!')
                socket.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
                socket.write("<h1>Internal Server Error</h1>")
            socket.close()


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
        if(line):
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

WebConfig()
