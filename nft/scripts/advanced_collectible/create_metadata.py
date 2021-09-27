from brownie import AdvancedCollectible
from pathlib import Path
import requests
import json

OPENSEA_URL = 'https://testnets.opensea.io/assets/{address}/{token_id}'
BREED_MAPPING = {
    0: 'PUG',
    1: 'SHIBA_INU',
    2: 'ST_BERNARD'
}

metadata_template = {
    "name": "",
    "c": "",
    "image_uri": "",
    "attributes": {"trait_type": "cuteness", "value": 100}
}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        ipfs_url = 'http://127.0.0.1:5001'
        endpoint = '/api/v0/add'
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1]
        uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(uri)
        return uri


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"{number_of_collectibles} of collectibles created")

    for token_id in range(number_of_collectibles):
        token_id = token_id + 1
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        print(f"TokenId {token_id} is a {breed}")
        meta = metadata_template
        meta['name'] = breed
        meta['description'] = f"An adorable {breed} pup"
        image_file_path = f"./img/{breed.lower().replace('_', '-')}.png"
        uri = upload_to_ipfs(image_file_path)
        meta['image_uri'] = uri
        meta_file_name = f"./metadata/{token_id}_{breed}.json"
        with open(meta_file_name, 'w') as f:
            json.dump(meta, f)
        print(meta)
        full_uri = upload_to_ipfs(meta_file_name)
        print(f"Uploaded meta to IPFS! {full_uri}")



