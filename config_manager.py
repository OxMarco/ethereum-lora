import os

class ConfigManager:
    """Centralised configuration manager."""
    
    @staticmethod
    def get_node_url():
        return os.environ.get('NODE_URL', 'http://127.0.0.1:8545')

    @staticmethod
    def get_lora_config():
        return {
            "lora_chip_model": os.environ.get('LORA_CHIP_MODEL', '400T33D'),
            "serial_port": os.environ.get('SERIAL_PORT', '/dev/serial0'),
            "aux_pin": int(os.environ.get('AUX_PIN', 18)),
            "m0_pin": int(os.environ.get('M0_PIN', 23)),
            "m1_pin": int(os.environ.get('M1_PIN', 24)),
            "address": int(os.environ.get('ADDRESS', 1)),
            "channel": int(os.environ.get('CHANNEL', 23)),
            "delimiter": os.environ.get('DELIMITER', '\n')
        }
