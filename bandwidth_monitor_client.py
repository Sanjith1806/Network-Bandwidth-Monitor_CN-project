import tkinter as tk
from tkinter import ttk
import psutil
import socket
import ssl
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BandwidthMonitorClient:
    def __init__(self, host, port, certfile):
        self.host = host
        self.port = port
        self.certfile = certfile

        self.root = tk.Tk()
        self.root.title("Network Bandwidth Monitor")

        self.label = ttk.Label(self.root, text="Network Bandwidth")
        self.label.pack()

        self.sent_label = ttk.Label(self.root, text="Sent: 0 bytes")
        self.sent_label.pack()

        self.received_label = ttk.Label(self.root, text="Received: 0 bytes")
        self.received_label.pack()

        self.fig, self.ax = plt.subplots()
        self.graph = FigureCanvasTkAgg(self.fig, master=self.root)
        self.graph.get_tk_widget().pack()

        self.start_button = ttk.Button(self.root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack()

        self.stop_button = ttk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack()

        self.running = False
        self.sent_data = []
        self.received_data = []
        self.timestamps = []

    def update_plot(self):
        sent_diff = [0]  # Initialize with 0 as there's no difference for the first data point
        received_diff = [0]  # Initialize with 0 as there's no difference for the first data point
        for i in range(1, len(self.sent_data)):
            sent_diff.append(self.sent_data[i] - self.sent_data[i-1])
            received_diff.append(self.received_data[i] - self.received_data[i-1])
            
        self.ax.clear()
        self.ax.plot(self.timestamps, sent_diff, label="Sent Difference")
        self.ax.plot(self.timestamps, received_diff, label="Received Difference")
        self.ax.legend()
        self.graph.draw()

    def start(self):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile=self.certfile)
        context.check_hostname = False  # Disable hostname verification
        context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_socket = context.wrap_socket(client_socket, server_hostname=self.host)
            ssl_socket.connect((self.host, self.port))
        except Exception as e:
            print("Error establishing SSL connection:", e)
            return

        start_time = time.time()

        while True:
            try:
                network_data = psutil.net_io_counters()
                total_bytes_sent = network_data.bytes_sent
                total_bytes_received = network_data.bytes_recv

                current_time = time.time() - start_time

                self.sent_label.config(text="Sent: {} bytes".format(total_bytes_sent))
                self.received_label.config(text="Received: {} bytes".format(total_bytes_received))

                self.sent_data.append(total_bytes_sent)
                self.received_data.append(total_bytes_received)
                self.timestamps.append(current_time)
                self.update_plot()

                ssl_socket.sendall(str(total_bytes_received).encode())
                ack = ssl_socket.recv(1024)
                time.sleep(1)

                if not self.running:
                    break
            except Exception as e:
                print("Error:", e)
                break

        try:
            ssl_socket.close()
        except Exception as e:
            print("Error closing SSL socket:", e)

    def start_monitoring(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.start).start()

    def stop_monitoring(self):
        self.running = False

if __name__ == "__main__":
    client = BandwidthMonitorClient('10.0.0.7', 8080, 'client_cert.pem')
    client.root.mainloop()
