from lora.lora_e22 import LoRaE22, Configuration
from lora.lora_e22_constants import FixedTransmission, RssiEnableByte, RssiAmbientNoiseEnable, RepeaterModeEnableByte, TransmissionPower33, AirDataRate

server_address = 0x00
client_address = 0x01
channel = 23

def configure(lora: LoRaE22, chipset: str, address) -> bool:
    configuration_to_set = Configuration(chipset)
    configuration_to_set.OPTION.RSSIAmbientNoise = RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_ENABLED
    configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
    configuration_to_set.TRANSMISSION_MODE.enableRepeater = RepeaterModeEnableByte.REPEATER_DISABLED
    configuration_to_set.OPTION.transmissionPower = TransmissionPower33.POWER_33
    configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
    configuration_to_set.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_111_625
    configuration_to_set.ADDH = 0x00
    configuration_to_set.ADDL = address
    configuration_to_set.CHAN = channel

    code, confSetted = lora.set_configuration(configuration_to_set)
    if code != 1:
        print("Configuration error")
        return False
    else:
        print("Configuration correctly set")
        return True
