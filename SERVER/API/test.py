# https://github.com/bjarne-hansen/py-nrf24/blob/master/test/simple-sender.py

from datetime import datetime

from flask import Flask
from flask_cors import CORS

import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *


app = Flask(__name__)
CORS(app)


@app.route('/turnOnLight', methods=['GET'])
def turn_on_light():
    print("Turning on light...")
    send_data(1)
    # Your script logic here
    return "Light turned on"

@app.route('/turnOffLight', methods=['GET'])
def turn_off_light():
    print("Turning off light...")
    send_data(0)
    # Your script logic here
    return "Light turned off"        

def send_data(data: int) -> None:
    try:
        print(f"Send to {address}")

        payload = struct.pack("<Bf", 0x01, data)

        nrf.reset_packages_lost()
        nrf.send(payload)
        try:
            nrf.wait_until_sent()
        except TimeoutError:
            print("Timeout waiting for transmission to complete.")

        if nrf.get_packages_lost() == 0:
            print(
                f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}"
            )
        else:
            print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")

    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()


def receive_data() -> None:
    try:
        print(f"Receive from {address}")

        while nrf.data_ready:
            now = datetime.now()

            # Read pipe and payload for message.
            pipe = nrf.data_pipe()
            payload = nrf.get_payload()

            hex = ":".join(f"{i:02x}" for i in payload)

            # Show message received as hex.
            print(
                f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}"
            )

            if len(payload) > 0:
                values = struct.unpack("<Bf", payload)
                print(f"Protocol: {values[0]}, data: {values[0]}")

            # Sleep 100 ms.
            time.sleep(0.1)

    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()


if __name__ == "__main__":
    # ---- Setup NRF24L01 ----
    hostname = "framboos20.local"
    port = 8888
    address = "1Node"

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
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

    nrf.show_registers()

    app.run(host='0.0.0.0', port=3000)

    print("Server is listening on port 3000...")

    while True:
        pass
        # receive_data()
