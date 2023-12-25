import socket
import ssl

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 3000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Wrap the socket with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='path/to/your/certificate.pem', keyfile='path/to/your/private.key')
server_socket = context.wrap_socket(sock, server_side=True)

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
