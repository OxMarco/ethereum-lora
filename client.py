import time
import json
import logging

from config_manager import ConfigManager
from lora_controller import LoRaController, MessageType

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

    server_address = 0x00
    waiting = False

    # get server address
    logging.info("Send ping")
    lora_controller.send_ping()
    while True:
        msg = lora_controller.listen()
        type, addr = lora_controller.parse_message_type(msg)
        if addr and type == MessageType.HANDSHAKE_REPLY.value:
            server_address = addr
            break
    logging.info("Server address acquired")

    # start main loop
    logging.info("Start main loop")
    while True:
        while waiting:
            msg = lora_controller.listen()
            if msg:
                logging.info(f"Message: {msg}")
                waiting = False

            if time.time() - start_time > 10:
                logging.warning("Timeout after waiting for 10 seconds.")
                waiting = False

        payload = get_user_payload()
        if payload:
            try:
                lora_controller.send_message(payload, server_address)
                waiting = True
                start_time = time.time()
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
