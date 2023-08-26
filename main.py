import time
import json
import requests
import logging

from config_manager import ConfigManager
from lora_controller import LoRaController
from node_connector import NodeConnector

logging.basicConfig(level=logging.INFO)

def main():
    node_url = ConfigManager.get_node_url()
    node = NodeConnector(node_url)
    node.test_connection()

    lora_config = ConfigManager.get_lora_config()
    lora_controller = LoRaController(**lora_config)
    lora_controller.setup()

    while True:
        msg = lora_controller.listen()
        if msg:
            try:
                response = node.send(msg)
                data = json.dumps(response, separators=(',', ':'))
                logging.info(f"Data: {data}")
                lora_controller.send_message(data)
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
            finally:
                time.sleep(2)

if __name__ == "__main__":
    main()
