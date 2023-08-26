import json
import requests
import os
import serial
import time

from lora.lora_e22 import LoRaE22, Configuration
from lora.lora_e22_operation_constant import ResponseStatusCode
from lora.lora_e22_constants import FixedTransmission, RssiEnableByte

from configure import configure, server_address

def test_connection():
    print("Testing connection to the node...", end='', flush=True)

    method = "web3_clientVersion"
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": [],
        "id": 1,
    }
    response = send_to_node(json.dumps(payload))
    if response != "":
        print("\nConnection successful!")
        print("Client Version:", response["result"])
    else:
        print("\nConnection failed! Please ensure your node is running and accessible.")
        exit(1)


def send_to_node(data):
    try:
        url = os.environ.get('NODE_URL', 'http://127.0.0.1:8545')
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()

        return response.json()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""


def main():
    try:
        test_connection()

        lora_chip_model = os.environ.get('LORA_CHIP_MODEL', '400T33D')
        serial_port = os.environ.get('SERIAL_PORT', '/dev/serial0')
        aux_pin = int(os.environ.get('AUX_PIN', 18))
        m0_pin = int(os.environ.get('M0_PIN', 23))
        m1_pin = int(os.environ.get('M1_PIN', 24))

        print("LoRa E22 setup...")
        lora_serial = serial.Serial(serial_port)
        lora = LoRaE22(lora_chip_model, lora_serial, aux_pin=aux_pin, m0_pin=m0_pin, m1_pin=m1_pin)
        code = lora.begin()
        if code != 1:
            print("LoRa interfacing error!")
            return

        configure(lora, lora_chip_model, server_address)

        if code != 1:
            print("LoRa setup error!")
            return
        print("OK")

        print("Listener started...")
        print("\n------------------\n")
                
        while True:
            if lora.available() > 0:
                code, msg, rssi = lora.receive_message(rssi=True, delimiter=b'\n')
                print("Received a new message")
                if code != 1:
                    print("Error!")
                    continue
                
                print("RSSI", rssi)
                try:
                    # remove eventual spurious chars
                    start_idx = msg.find('{')
                    msg = msg[start_idx:].strip()
                    
                    try:
                        print("Sending to node...")
                        response = send_to_node(msg)
                        print("Response: ", json.dumps(response, indent=4))
                        #print("Responding...")
                        #code = lora.send_transparent_message(response)
                        #if code != 1:
                        #    print("Error!")
                        #print("OK")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                        continue
                    finally:
                        time.sleep(2)
                except json.JSONDecodeError as e:
                    print(f"Decoding error: {e}")
                    continue
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return


if __name__ == "__main__":
    main()
