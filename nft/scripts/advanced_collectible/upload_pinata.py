import os
import requests

from pathlib import Path

PINATA_BASE_URL = 'https://api.pinata.cloud'

def main():
    upload_to_pinata()

def upload_to_pinata():
    filepaths = [
        "./img/pug.png",
        "./img/st-bernard.png",
        "./img/shiba-inu.png"
    ]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")
    }
    endpoint = '/pinning/pinFileToIPFS'
    for filepath in filepaths:
        filename = filepath.split("/")[-1]
        with Path(filepath).open('rb') as fp:
            image_binary = fp.read()
            response = requests.post(
                PINATA_BASE_URL + endpoint,
                files={"file": (filename, image_binary)},
                headers=headers
            )
