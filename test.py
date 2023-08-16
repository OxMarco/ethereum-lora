import os
import serial

from lora.lora_e22 import LoRaE22, Configuration
from lora.lora_e22_operation_constant import ResponseStatusCode
from lora.lora_e22_constants import FixedTransmission, RssiEnableByte

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
    
    configuration_to_set = Configuration(lora_chip_model)
    # To enable RSSI, you must also enable RSSI on receiver
    configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
    code, confSetted = lora.set_configuration(configuration_to_set)

    if code != 1:
        print("LoRa setup error!")
        return
    print("OK")

    payload = {
        "jsonrpc": "2.0",
        "method": "web3_clientVersion",
        "params": [],
        "id": 1
    }
    code = lora.send_transparent_dict(payload)


if __name__ == "__main__":
    main()
