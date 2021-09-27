from brownie import AdvancedCollectible, network
from pathlib import Path
import requests
import json

from scripts.advanced_collectible.deploy import get_account, OPENSEA_URL

from requests.api import get

OPENSEA_URL = 'https://testnets.opensea.io/assets/{address}/{token_id}'
BREED_MAPPING = {
    0: 'PUG',
    1: 'SHIBA_INU',
    2: 'ST_BERNARD'
}

dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/QmVCfUye9XvFir31cqmyXPaEiRdFLLoXEC4WQ62Ne2iTGM?filename=10_PUG.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmVhVwCVcDm5ZuBGSXaoEMXY3fKEenLJA4UVXBwEDeZw82?filename=8_ST_BERNARD.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/Qmcqzs3m5eyFjqWTnBmw82rb1ZVyE6bsTg6bRSHQoL2T17?filename=6_SHIBA_INU.json"
}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def set_token_uri(token_id, nft_contract, uri):
    print(f"Setting tokenURI of {token_id}")
    account = get_account()
    print(nft_contract.tokenIdToBreed(token_id))
    tx = nft_contract.setTokenURI(token_id, uri, {"from": account})
    tx.wait(1)
    url = OPENSEA_URL.format(
        address=nft_contract.address,
        token_id=token_id
    )
    print(f"URI deployed. You can see your NFT at: {url}")
    print("Wait up to 20mins")


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"{number_of_collectibles} of collectibles created")
    print("################\n")
    for token_id in range(number_of_collectibles):
        token_id = token_id
        print(f"TokenId: {token_id}")
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        print(advanced_collectible.tokenURI(token_id))
        # if not advanced_collectible.tokenURI(token_id).startswith("https://"):
        #     set_token_uri(token_id, advanced_collectible, dog_metadata_dict[breed])
        #     print("\n################\n")
        set_token_uri(token_id, advanced_collectible, dog_metadata_dict[breed])
        print("\n################\n")



