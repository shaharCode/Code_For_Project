import socket
import Scan

# Establishing the server and handling the communication with the client
class ScanServer:
    # Creating the Class object for 'Server'
    def __init__(self, ip, port=4444):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Handles the communication between the server and the client
    def Run_Server(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen() # waiting for clients
        conn, addr = self.sock.accept()
        # sending and receiving messages
        while True:
            try:
                msg = conn.recv(1024).decode()
                data = Scan.Scan(msg) # Sending the received message (Vulnerability type) to be tested
                # conn.send(data.encode())
                conn.send(data)
            except Exception as e:
                print(e)





