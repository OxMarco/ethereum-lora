import time
import json
import logging

from config_manager import ConfigManager
from lora_controller import LoRaController

logging.basicConfig(level=logging.INFO)

def get_user_payload():
    payload = input("\nPlease enter the JSON payload: ")
    try:
        json.loads(payload)
        return payload
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON input {e}")
        return None

def main():
    lora_config = ConfigManager.get_lora_config()
    lora_controller = LoRaController(**lora_config)
    lora_controller.setup()

    waiting = False

    while True:
        while waiting:
            message = lora_controller.listen()
            if message:
                logging.info(f"Message: {message}")
                time.sleep(2)
                waiting = False

            if time.time() - start_time > 10:
                logging.warning("Timeout after waiting for 10 seconds.")
                waiting = False

        payload = get_user_payload()
        if payload:
            try:
                lora_controller.send_message(payload, 0x00)
                waiting = True
                start_time = time.time()
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
