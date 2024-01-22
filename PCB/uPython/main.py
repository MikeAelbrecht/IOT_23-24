import usys
import ustruct as struct
import utime
from machine import Pin, SPI, SoftSPI
from nrf24l01 import NRF24L01
from micropython import const
import machine

# RGB led connected to RP2040
LED_R = Pin(0, Pin.OUT)
LED_G = Pin(1, Pin.OUT)
LED_B = Pin(2, Pin.OUT)

# PIR sensor connected to RP2040
PIR_IN = Pin(3, Pin.IN, Pin.PULL_DOWN)

# Boost converter connected to RP2040
B_EN = Pin(9, Pin.OUT)
B_IADJ = Pin(10, Pin.OUT)

# NRF24L01+ radio connected to RP2040
MISO_PIN = Pin(4)
CE_PIN = Pin(5)
SCK_PIN = Pin(6)
MOSI_PIN = Pin(7)
CSN_PIN = Pin(8)

_RX_POLL_DELAY = const(15)
_RESPONDER_SEND_DELAY = const(10)

# NRF24L01 radio configuration
print("Initializing NRF24L01 radio...")
spi = SPI(0, sck=SCK_PIN, mosi=MOSI_PIN, miso=MISO_PIN)
nrf = NRF24L01(spi, CSN_PIN, CE_PIN, payload_size=4)

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])

print("NRF24L01 radio initialized")


def is_motion_detected():
    return PIR_IN.value() == 1


def send_data(data):
    nrf.stop_listening()
    print("sending data: ", data)

    try:
        data = struct.pack("i", data)
        nrf.send(data)
    except OSError:
        pass

    nrf.start_listening()


def receive_data():
    if nrf.any():
        print("received data")
        while nrf.any():
            buf = nrf.recv()
            data = struct.unpack("i", buf)
            print("received:", data)

            utime.sleep_ms(_RX_POLL_DELAY)

        # Give initiator time to get into receive mode.
        utime.sleep_ms(_RESPONDER_SEND_DELAY)
        nrf.stop_listening()

        # try:
        #     nrf.send(struct.pack("i", 1))
        # except OSError:
        #     pass

        # print("sent response")
        # utime.sleep_ms(_RESPONDER_SEND_DELAY)
        nrf.start_listening()


if __name__ == "__main__":
    print("Starting main loop...")
    nrf.start_listening()

    while True:
        receive_data()

        if is_motion_detected():
            print("motion detected")
            send_data(1)
