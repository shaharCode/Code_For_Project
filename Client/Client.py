import socket
from Cryptographer import Cryptographer


class Client:
    # Creating the Class object for 'Client'
    def __init__(self, ip, port = 4444):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_status = False

    # Establishing a connection to the server
    def connect_to_server(self):
        try:
            self.sock.connect((self.ip,self.port))
            self.connection_status = True
        except:
            self.connection_status = False



    # Sending the received data to the server
    def send_data(self, data):
        self.sock.send(data.encode())

    # Receiving encrypted data from the server and returning it decrypted
    def recv_enc(self):
        data = self.sock.recv(1024)
        decryptor = Cryptographer()
        result = decryptor.decrypt_message(data)
        return result

    # Receiving data from the server and returning it
    def recv(self):
        return self.sock.recv(1024).decode()

