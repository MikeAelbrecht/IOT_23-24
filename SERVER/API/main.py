from datetime import datetime

from flask import Flask
from flask_cors import CORS

import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *

import mysql.connector


app = Flask(__name__)
CORS(app)

database = mysql.connector.connect(
    host="localhost",
    user="iot",
    password="iot",
    database="iot"
)

cursor = database.cursor()


def insert_data():
    query = "INSERT INTO waarden (datum, tijd) VALUES (%s, %s)"
    values = (datetime.datetime.now().date(), datetime.datetime.now().time())

    cursor.execute(query, values)

    database.commit()

@app.route('/turnOnLight', methods=['GET'])
def turn_on_light():
    print("Turning on light...")

    resp = False
    while not resp:
        resp = send_data(1)
    return "Light turned on"

@app.route('/turnOffLight', methods=['GET'])
def turn_off_light():
    print("Turning off light...")

    resp = False
    while not resp:
        resp = send_data(0)
    return "Light turned off"        

def send_data(data: int) -> bool:
    try:
        payload = struct.pack("i", data)

        nrf.reset_packages_lost()
        nrf.send(payload)

        try:
            nrf.wait_until_sent()
        except TimeoutError:
            print("Timeout waiting for transmission to complete.")

        time.sleep(0.1)

        if nrf.get_packages_lost() == 0:
            print(
                f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}"
            )
            return True
        else:
            print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
            return False

    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()


def receive_data() -> None:
    try:
        while nrf.data_ready:
            now = datetime.now()

            # Read pipe and payload for message.
            pipe = nrf.data_pipe()
            payload = nrf.get_payload()

            print(
                f"{now:%Y-%m-%d %H:%M:%S}: pipe: {pipe}, len: {len(payload)} bytes"
            )

            if len(payload) > 0:
                values = struct.unpack("i", payload)
                print(f"data: {values[0]}")

                if values[0] == 1:
                    insert_data()

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
    
    pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

    print(f"Connecting to GPIO daemon on {hostname}:{port} ...")
    pi = pigpio.pi(hostname, port)

    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    nrf = NRF24(
        pi,
        ce=25,
        payload_size=4,
        channel=46,
        data_rate=RF24_DATA_RATE.RATE_250KBPS,
        pa_level=RF24_PA.LOW
    )

    # nrf.set_address_bytes(len(send_address))
    nrf.open_writing_pipe(pipes[1])
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, pipes[0])

    # nrf.show_registers()

    app.run(host='0.0.0.0', port=3000)

    print("Server is listening on port 3000...")
    try:
        while True:
            receive_data()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected ... goodbye.")
        pi.stop()
