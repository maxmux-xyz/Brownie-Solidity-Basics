from brownie import SimpleStorage, config, network, accounts
import time

def main():
    net = network.show_active()
    print(net)
    if net == 'rinkeby':
        account = accounts.add(config['wallets']['from_key'])
        print(account)
        # Deploying contract
        simple_storage = SimpleStorage.deploy({"from":account})
        print(simple_storage)
    elif net == 'local':
        # We will be running this on local ganache only.
        account = accounts[0]
        print(account)
        # Deploying contract
        simple_storage = SimpleStorage.deploy({"from":account})
        print(simple_storage)
