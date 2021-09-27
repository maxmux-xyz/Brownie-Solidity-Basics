from brownie import (
    config,
    network,
    MyToken,
    accounts,
)
from web3 import Web3

FORKED_LOCAL_ENVIRONEMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONEMENTS = ['development', 'ganache-local']

def get_account(index=None, id=None):
    net = network.show_active()
    print(f"Network: {net}")

    if index:
        return accounts[index]
    if id:
        accounts.load(id)
    if (net in FORKED_LOCAL_ENVIRONEMENTS
        or net in LOCAL_BLOCKCHAIN_ENVIRONEMENTS):
        return accounts[0]
    return accounts.add(config['wallets']['from_key'])

def deploy_token():
    account = get_account()
    initial_supply = Web3.toWei(1000, 'ether')
    token = MyToken.deploy(
        initial_supply,
        {"from": account},
        publish_source=config['networks'][network.show_active()].get('verify', False),
    )
    print(f"Deployed MyToken contract: {token}")
    print(f"Token name: {token.name()}")
    return token



def main():
    token = deploy_token()

