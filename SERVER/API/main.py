import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ("localhost", 3000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening on port 3000...")

while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()

    # Receive data from the client
    data = client_socket.recv(1024).decode("utf-8")

    # Process the received data
    print("Received data:", data)

    # Send a response back to the client
    response = "Hello from the server!"
    client_socket.sendall(response.encode("utf-8"))

    # Close the connection
    client_socket.close()
