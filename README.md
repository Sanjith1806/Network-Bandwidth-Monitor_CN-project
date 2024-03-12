This Python application demonstrates a network bandwidth monitoring system consisting of a server and a client. The server collects data from connected clients, while the client sends network data to the 
server for monitoring

Requirements:
Python 3.x
tkinter (Python's standard GUI library)
matplotlib (for plotting graphs)
psutil (for retrieving system/network information)
valid SSL certificate on both client and server


Usage: Download source code files, install given dependencies using 'pip', run the server and client. The GUI window will appear shopwing real time network bandwidth data

Components:
Server (BandwidthMonitorServer):
Listens for incoming connections from clients. Accepts clients and handles communication with them. Collects network data from clients and updates its data queues. Uses SSL/TLS for secure communication.

Client (BandwidthMonitorClient):
Connects to the server. Sends network data (bytes received) to the server for monitoring. Continuously sends network data to the server. Uses SSL/TLS for secure communication.

GUI (NetworkBandwidthMonitorGUI):
Provides a graphical user interface for monitoring network bandwidth. Displays a real-time graph of combined sent and received data. Allows starting and stopping of monitoring.


File Structure:
bandwidth_monitor.py: Main Python script containing the server, client, and GUI classes.
localhost_cert.pem: SSL/TLS certificate file (for demonstration purposes).
localhost_key.pem: SSL/TLS private key file (for demonstration purposes).
README.md: Documentation file.
