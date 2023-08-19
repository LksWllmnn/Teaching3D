import socket

server_ip = "127.0.0.1"  # Replace with the C# server's IP address
server_port = 12345  # Replace with the C# server's port

data_to_send = "Hello from Python!"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_ip, server_port))
    client_socket.send(data_to_send.encode())