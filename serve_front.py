import os
import threading
import http.server
import socketserver
from settings import BASE_DIR

if __name__ == "__main__":
    os.chdir(BASE_DIR+"\\frontend\\public") # changing to frontend dir to serve that only
    PORTS = [8000, 8001, 8002, 8003, 8004, 8005]
    for PORT in PORTS:
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        thread = threading.Thread(target=httpd.serve_forever)
        thread.start()
    print("serving at ports: ", " ".join(map(str, PORTS)))


