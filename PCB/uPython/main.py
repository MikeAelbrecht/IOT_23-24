import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const
import asyncio

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

# Receiver
nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])

print("NRF24L01 radio initialized")

# Variable for the light
light_master = False


def is_motion_detected() -> bool:
    return PIR_IN.value() == 1


async def turn_on_light(duration: int) -> None:
    if not light_master:
        LED_B.value(1)
        await asyncio.sleep(duration)
        LED_B.value(0)


def send_data(data) -> None:
    nrf.stop_listening()
    print("Sending data:", data)

    try:
        data = struct.pack("i", data)
        nrf.send(data)
    except OSError:
        pass

    # start listening again
    nrf.start_listening()

    # wait for response, with 250ms timeout
    start_time = utime.ticks_ms()
    timeout = False

    while not nrf.any() and not timeout:
        if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
            timeout = True

    if timeout:
        print("Failed, response timed out")
    else:
        print("Success, got response")

        data = nrf.recv()
        data = struct.unpack("i", data)

        print("Received response:", data)


def receive_data() -> None:
    global light_master
    if nrf.any():
        print("Received data")

        while nrf.any():
            buf = nrf.recv()
            data = struct.unpack("i", buf)
            print("Received:", data)

            LED_B.value(data)
            light_master = True

            utime.sleep_ms(_RX_POLL_DELAY)

        # Give initiator time to get into receive mode.
        utime.sleep_ms(_RESPONDER_SEND_DELAY)
        nrf.stop_listening()

        try:
            data = struct.pack("i", 1)
            nrf.send(data)
        except OSError:
            pass

        nrf.start_listening()


if __name__ == "__main__":
    print("Starting main loop...")
    LED_B.value(1)
    utime.sleep_ms(500)
    LED_B.value(0)
    nrf.start_listening()

    while True:
        receive_data()

        if is_motion_detected():
            print("motion detected")
            send_data(1)
            asyncio.run(turn_on_light(5))
