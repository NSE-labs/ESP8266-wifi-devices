
# Begin configuration
TITLE    = "Test Input"
# End configuration

import machine
import usocket
import micropython

micropython.alloc_emergency_exception_buf(100)


def ok(socket, query):
    socket.write("HTTP/1.1 OK\r\n\r\n")
    socket.write("<!DOCTYPE html><html><title>"+TITLE+"</title><body>")
    socket.write("<form method='POST' action='/action?'>")
    socket.write("  Access point: <input type='text' name='ap'>")
    socket.write("<input type='submit' value='Submit'>")
    socket.write("</form></body></html>")
                 

def err(socket, code, message):
    socket.write("HTTP/1.1 "+code+" "+message+"\r\n\r\n")
    socket.write("<h1>"+message+"</h1>")

                 
def handle(socket):
    (method, url, version) = socket.readline().split(b" ")
    print(method, url, version)
    if b"?" in url:
        (path, query) = url.split(b"?", 2)
    else:
        (path, query) = (url, b"")
    print(path, query)
    while True:
        header = socket.readline()
        if header == b"":
            return
        if header == b"\r\n":
            break
    print('Handling it')
    if version != b"HTTP/1.0\r\n" and version != b"HTTP/1.1\r\n":
        err(socket, "505", "Version Not Supported")
    elif method == b"GET":
        if path == b"/":
            ok(socket, query)
        else:
            err(socket, "404", "Not Found")
    elif method == b"POST":
        if path == b"/action":
            print('Calling ok')
            ok(socket, query)
        else:
            err(socket, "404", "Not Found")
    else:
        err(socket, "501", "Not Implemented")

server = usocket.socket()
server.bind(('0.0.0.0', 8080))
server.listen(1)
while True:
    try:
        (socket, sockaddr) = server.accept()
        print("Received request")
        handle(socket)
    except:
        socket.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
        socket.write("<h1>Internal Server Error</h1>")
    socket.close()
