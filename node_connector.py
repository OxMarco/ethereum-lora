import json
import logging
import requests

class NodeConnector:
    def __init__(self, url):
        self.url = url

    def test_connection(self):
        logging.info("Testing connection to the node...")
        method = "web3_clientVersion"
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": [],
            "id": 1,
        }
        response = self.send(json.dumps(payload, separators=(',', ':')))
        if response:
            logging.info(f"Connection successful!\nClient Version: {response['result']}")
        else:
            logging.error("Connection failed! Please ensure your node is running and accessible.")
            exit(1)

    def send(self, data):
        logging.info("Sending to node...")
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.url, data=data, headers=headers)
        logging.info("OK")

        return response.json()
