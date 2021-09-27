from web3 import Web3
from brownie import (
    AdvancedCollectible
)
from scripts.advanced_collectible.deploy import get_account, fund_with_link

def main():
    create()

def create():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creating_tx = advanced_collectible.createCollectible(
        "None",
        {"from": account}
    )
    creating_tx.wait(1)
    print("NFT has been created!")
