import os
import json
import serial

from lora.lora_e22 import LoRaE22, Configuration
from lora.lora_e22_operation_constant import ResponseStatusCode
from lora.lora_e22_constants import FixedTransmission, RssiEnableByte

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

    while True:
        # Prompt the user to enter JSON payload
        payload = input("\nPlease enter the JSON payload (or 'exit' to quit): ")

        if payload.strip().lower() == 'exit':
            break

        # Validate the input to ensure it's a valid JSON
        try:
            json.loads(payload)

            print("Sending message...")
            code = lora.send_fixed_message(0, server_address, channel, json.dumps(payload)+'\n')
            if code != 1:
                print("Error!")
            print("OK")

        except json.JSONDecodeError:
            print("Invalid JSON input, retry")
        continue


if __name__ == "__main__":
    main()
