from brownie import StorageFactory, config, accounts, network
import time

def main():
    net = network.show_active()
    print(f"Network: {net}")
    if net == 'local':
        # We will be running this on local ganache only.
        account = accounts[0]
        # print(account)

        # Deploying contract
        storage_factory_address = "0x7c0d82D784aEB6947BC8E23DC25cBB9661514E6A"
        print(f"Getting StorageFactory contract at address {storage_factory_address}")
        storage = StorageFactory.at(storage_factory_address)
        # print(storage)

        print("\nCreating SimpleStorage with StorageFactory")
        storage.CreateSimpleStorageContract({"from":account})
        print(storage.simpleStorageArray(0))

        print("\nSetting number in SimpleStorage")
        storage.SFStore(0, 4, {"from":account})

        print("\nReading Simple storage number")
        print(storage.SFGet(0))
