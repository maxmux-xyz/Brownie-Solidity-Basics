from brownie import SimpleStorage, config, accounts, network
import time

def main():
    net = network.show_active()
    print(net)
    if net == 'rinkeby':
        account = accounts.add(config['wallets']['from_key'])
        simple_storage = SimpleStorage[-1]
        # Set number
        simple_storage.setNumber(12, {"from":account})
        # Get number
        print(simple_storage.getNumber())
        # Add person to People array at 0th position
        simple_storage.addPeople(12, "Maxime", {"from":account})
        time.sleep(3)
        print(simple_storage.pple(0))
        # Add person to People array at 1st position
        simple_storage.addPeople(10, "Clementine", {"from":account})
        time.sleep(3)
        print(simple_storage.pple(1))
        print(simple_storage.nameToFavNumber("Clementine"))
    elif net == 'local':
        # We will be running this on local ganache only.
        account = accounts[0]
        print(account)
        # Deploying contract
        simple_storage = SimpleStorage.at('0x0F7A34844fC4Ca81928Add231796CEEfB91D0982')
        print(simple_storage)
        # Set number
        simple_storage.setNumber(12, {"from":account})
        # Get number
        print(simple_storage.getNumber())
        # Add person to People array at 0th position
        simple_storage.addPeople(12, "Maxime", {"from":account})
        time.sleep(3)
        print(simple_storage.pple(0))
        # Add person to People array at 1st position
        simple_storage.addPeople(10, "Clementine", {"from":account})
        time.sleep(3)
        print(simple_storage.pple(1))
        print(simple_storage.nameToFavNumber("Clementine"))

