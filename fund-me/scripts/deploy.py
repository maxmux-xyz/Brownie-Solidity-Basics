from brownie import FundMe, config, network, accounts
import time

def main():
    net = network.show_active()
    print(f"Network: {net}")
    if net == 'local':
        # We will be running this on local ganache only.
        account = accounts[0]
        print(account)
        # Deploying contract
        fund_me = FundMe.deploy({"from":account})
        print(fund_me)
    if net == 'rinkeby':
        # We will be running this on local ganache only.
        account = accounts.add(config['wallets']['from_key'])
        print(account)
        # Deploying contract
        fund_me = FundMe.deploy({"from":account})
        print(fund_me)
