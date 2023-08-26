import serial
import logging

from lora.lora_e22 import LoRaE22, Configuration
from lora.lora_e22_constants import FixedTransmission, RssiEnableByte, RssiAmbientNoiseEnable, RepeaterModeEnableByte, TransmissionPower33, AirDataRate, UARTParity, UARTBaudRate

class LoRaController:
    def __init__(self, lora_chip_model, serial_port, aux_pin, m0_pin, m1_pin, address, channel, delimiter='\n'):
        self.lora_chip_model = lora_chip_model
        self.serial_port = serial_port
        self.aux_pin = aux_pin
        self.m0_pin = m0_pin
        self.m1_pin = m1_pin
        self.address = address
        self.channel = channel
        self.delimiter = delimiter

        self.lora_serial = serial.Serial(self.serial_port)
        self.lora = LoRaE22(self.lora_chip_model, self.lora_serial, aux_pin=self.aux_pin, m0_pin=self.m0_pin, m1_pin=self.m1_pin)

    def setup(self):
        logging.info("LoRa E22 setup...")
        code = self.lora.begin()
        if code != 1:
            logging.error("LoRa interfacing error!")
            exit(1)

        configuration_to_set = Configuration(self.lora_chip_model)
        configuration_to_set.OPTION.RSSIAmbientNoise = RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_ENABLED
        configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
        configuration_to_set.TRANSMISSION_MODE.enableRepeater = RepeaterModeEnableByte.REPEATER_DISABLED
        configuration_to_set.OPTION.transmissionPower = TransmissionPower33.POWER_33
        configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
        # configuration_to_set.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_100_96
        configuration_to_set.ADDH = 0x00
        configuration_to_set.ADDL = self.address
        configuration_to_set.CHAN = self.channel
        configuration_to_set.SPED.uartParity = UARTParity.MODE_00_8N1
        configuration_to_set.SPED.uartBaudRate = UARTBaudRate.BPS_9600

        code, confSetted = self.lora.set_configuration(configuration_to_set)
        if code != 1:
            logging.error("Configuration error")
            exit(1)
        logging.info("OK")

    def listen(self):
        if self.lora.available() > 0:
            code, msg, rssi = self.lora.receive_message(rssi=True, delimiter=b'\n')
            if code == 1:
                logging.info(f"Received new message with RSSI {rssi}")
                start_idx = msg.find('{')
                msg = msg[start_idx:].strip()
                return msg
            else:
                logging.error("Error receiving message!")

    def send_message(self, payload, destination_address):
        logging.info("Sending message...")
        code = self.lora.send_fixed_message(0, destination_address, self.channel, payload + self.delimiter)
        if code != 1:
            logging.error("Error sending message!")
            raise Exception("Error sending message")
        logging.info("OK")
