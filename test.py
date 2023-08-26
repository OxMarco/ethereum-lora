import os
import json
import serial
import time

from lora.lora_e22 import LoRaE22
from configure import configure, server_address, client_address, channel

def main():
    lora_chip_model = os.environ.get('LORA_CHIP_MODEL', '400T33D')
    serial_port = os.environ.get('SERIAL_PORT', '/dev/serial0')
    aux_pin = int(os.environ.get('AUX_PIN', 18))
    m0_pin = int(os.environ.get('M0_PIN', 23))
    m1_pin = int(os.environ.get('M1_PIN', 24))

    print("LoRa E22 setup...")
    loraSerial = serial.Serial(serial_port)
    lora = LoRaE22(lora_chip_model, loraSerial, aux_pin=aux_pin, m0_pin=m0_pin, m1_pin=m1_pin)
    code = lora.begin()
    if code != 1:
        print("LoRa interfacing error!")
        return
    
    configure(lora, lora_chip_model, client_address)

    waiting = False

    while True:
        while waiting:
            if lora.available() > 0:
                code, msg, rssi = lora.receive_message(rssi=True, delimiter=b'\n')
                print("Received a new message")
                if code != 1:
                    print("Error!")
                else:                
                    print("RSSI", rssi)

                    # remove eventual spurious chars
                    start_idx = msg.find('{')
                    msg = msg[start_idx:].strip()
                    print("Message", msg)
                    time.sleep(2)

                waiting = False

        # Prompt the user to enter JSON payload
        payload = input("\nPlease enter the JSON payload: ")

        # Validate the input to ensure it's a valid JSON
        try:
            json.loads(payload)

            print("Sending message...")
            code = lora.send_fixed_message(0, server_address, channel, payload+'\n')
            if code != 1:
                print("Error!")
            print("OK")
            waiting = True

        except json.JSONDecodeError as e:
            print(f"Invalid JSON input {e}")


if __name__ == "__main__":
    main()
