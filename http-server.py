# Filename:
#      http-server.py
#
# Descrition:
#      This program implements a bare HTTP server.
#
# Author:
#      Glenn G. Fabia
#      gfabia@gbox.adnu.edu.ph
#      Ateneo de Naga University
#
# Notes:
#      This is a handout for ITMC231 - Platform Technologies
#      Intersession S/Y 2020-2021

import sys
import socket

if len(sys.argv) < 2:
    print("Usage: {} port_no".format(sys.argv[0]))
    exit(1) 

port_no = int(sys.argv[1])

# Create a socket for incoming connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to a port
sock.bind(('localhost', port_no))

# Mark the socket so it will listen for incoming connections
sock.listen(5)

while True:
    # Accept new connection
    (conn, addr) = sock.accept()

    # Receive HTTP request
    http_request = conn.recv(1024).decode()
    # print("HTTP Request:", http_request)
    
    # Extract URL from HTTP request
    http_request_lines = http_request.split("\r\n")
    request_line = http_request_lines[0]
    method, URL, version = request_line.split(" ")
    URL = URL.strip("/")

    # If no URL specified, default to 'index.html'
    if URL == "":
        URL = "index.html"
    
    status_code, status_phrase = 200, "OK"
    try:
        # Open and read contents of requested file
        doc = open(URL, "r")
        doc_contents = doc.read()
        doc.close()
    except:
        # Error: Can't open file (File not found?)
        status_code, status_phrase = 404, "NOT_FOUND"

    # Send HTTP response
    http_response_lines = [
        "HTTP/1.1 {} {}".format(status_code, status_phrase),
        "Content-Type: text/html",
        "\r\n"
    ]    
    if status_code == 200:
        http_response_lines.append(doc_contents)
    else:
        http_response_lines.append("<html><body><h1>404</h1><p>Error: File not found.</p></body></html>")
    
    http_response = "\r\n".join(http_response_lines)
    conn.send(http_response.encode("utf-8"))

    # Close connection
    print(conn.getpeername()[0], ":", request_line, status_code)
    conn.close()
