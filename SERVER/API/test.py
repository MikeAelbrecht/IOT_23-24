# https://github.com/bjarne-hansen/py-nrf24/blob/master/test/simple-sender.py

import socket

def handle_data(data) -> None:
    print("Received data:", data)

    if ("/turnOnLight" in data):
        print("Turning on light...")
    elif ("/turnOffLight" in data):
        print("Turning off light...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_address = ('framboos20.local', 3000)
server_address = ('localhost', 3000)
sock.bind(server_address)

sock.listen(1)

print("Server is listening on port 3000...")

while True:
    # Wait for a connection
    client_socket, client_address = sock.accept()

    # Receive data from the client
    data = client_socket.recv(1024).decode("utf-8")

    handle_data(data)

    # Send a response back to the client
    response = "Hello from the server!"
    client_socket.sendall(response.encode("utf-8"))

    # Close the connection
    client_socket.close()
