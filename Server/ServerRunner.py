
import threading
import socket
from ScanServer import ScanServer
from SiteServer import app

# Server side runner
# Initiates the flask page and the server
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_ip = s.getsockname()[0]
    s.close()
    server_port = 4444
    scan_server = ScanServer(server_ip, server_port)
    th = threading.Thread(target=scan_server.Run_Server)
    th.start()
    app.run(port=80, host="0.0.0.0")

#Run Site and scan server in a thread
if __name__ == "__main__":
    main()