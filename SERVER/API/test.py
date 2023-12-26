# https://github.com/bjarne-hansen/py-nrf24/blob/master/test/simple-sender.py

import socket

import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *


def handle_data(data) -> None:
    print("Received data:", data)

    if "/turnOnLight" in data:
        print("Turning on light...")
        send_data(1)
    elif "/turnOffLight" in data:
        print("Turning off light...")
        send_data(0)


def send_data(data: int) -> None:
    try:
        print(f"Send to {address}")

        while True:
            payload = struct.pack("<Bff", 0x01, data)

            # Send the payload to the address specified above.
            nrf.reset_packages_lost()
            nrf.send(payload)
            try:
                nrf.wait_until_sent()
            except TimeoutError:
                print("Timeout waiting for transmission to complete.")
                # Wait 10 seconds before sending the next reading.
                time.sleep(10)
                continue

            if nrf.get_packages_lost() == 0:
                print(
                    f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}"
                )
            else:
                print(
                    f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}"
                )

            # Wait 10 seconds before sending the next reading.
            time.sleep(10)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()


if __name__ == "__main__":
    # ---- Setup NRF24L01 ----
    hostname = "framboos20.local"
    port = 8888
    address = "1SNSR"

    print(f"Connecting to GPIO daemon on {hostname}:{port} ...")
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    nrf = NRF24(
        pi,
        ce=25,
        payload_size=RF24_PAYLOAD.DYNAMIC,
        channel=100,
        data_rate=RF24_DATA_RATE.RATE_250KBPS,
        pa_level=RF24_PA.LOW,
    )
    nrf.set_address_bytes(len(address))
    nrf.open_writing_pipe(address)

    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    # ---- Setup API ----
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # server_address = ('framboos20.local', 3000)
    server_address = ("localhost", 3000)
    sock.bind(server_address)

    sock.listen(1)

    print("Server is listening on port 3000...")

    while True:
        client_socket, client_address = sock.accept()

        data = client_socket.recv(1024).decode("utf-8")

        handle_data(data)

        response = "Hello from the server!"
        client_socket.sendall(response.encode("utf-8"))

        client_socket.close()