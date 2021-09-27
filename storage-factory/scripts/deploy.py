from brownie import StorageFactory, config, network, accounts
import time

def main():
    net = network.show_active()
    print(net)
    if net == 'local':
        # We will be running this on local ganache only.
        account = accounts[0]
        print(account)
        # Deploying contract
        storage_factory = StorageFactory.deploy({"from":account})
        print(storage_factory)
