# bandwidth_monitor_server.py

import socket
import ssl
import threading
from collections import deque

class BandwidthMonitorServer:
    def __init__(self, host, port, certfile, keyfile):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.clients = []
        self.sent_data_queue = deque(maxlen=100)  
        self.received_data_queue = deque(maxlen=100)  

    def start(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Server listening on {}:{}".format(self.host, self.port))
        try:
            while True:
                client_socket, client_addr = server_socket.accept()
                client_ssl_socket = context.wrap_socket(client_socket, server_side=True)
                self.clients.append(client_ssl_socket)
                print("New client connected from {}:{}".format(*client_addr))
                threading.Thread(target=self.handle_client, args=(client_ssl_socket,)).start()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            server_socket.close()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                received_data = float(data.decode()) 
                self.received_data_queue.append(received_data)
                
                self.update_sent_data(received_data)
                
                client_socket.sendall(b"ACK")
            except ssl.SSLWantReadError:
                pass
            except ssl.SSLError:
                break

        print("Client disconnected.")
        self.clients.remove(client_socket)
        client_socket.close()

    def update_sent_data(self, data):
        self.sent_data_queue.append(data)

if __name__ == "__main__":
    server = BandwidthMonitorServer('192.168.93.35', 8080, 'localhost_cert.pem', 'localhost_key.pem')
    server.start()
