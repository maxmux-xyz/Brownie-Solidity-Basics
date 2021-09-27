from brownie import FundMe, config, accounts, network
from web3 import Web3

def main():
    net = network.show_active()
    print(f"Network: {net}")
    if net == 'local':
        # We will be running this on local ganache only.
        account = accounts[0]
        # print(account)

        # Getting deployed contract
        contract_address = "0x861686b472C66757B8668F2356969E287Dc5D810"
        print(f"Getting StorageFactory contract at address {contract_address}")
        fundMe = FundMe.at(contract_address)
        # print(fundMe)

        print("\nFunding the contract")
        fundMe.fund({"from":account, "amount": 1000000000000000000})
        print(f"{account}: {Web3.fromWei(fundMe.addressToAmountFunded(account), 'ether')}")
        print(Web3.fromWei(fundMe.balance(), 'ether'))
    if net == 'rinkeby':
        # We will be running this on local ganache only.
        account = accounts.add(config['wallets']['from_key'])
        # print(account)

        # Getting deployed contract
        fundMe = FundMe[-1]
        print(f"Getting StorageFactory contract at address {fundMe}")

        print(f"\nAggregatorV3 version:{fundMe.getVersion()}")

        print("\nGetting ETH/USD price..")
        price = fundMe.getPrice()
        print(price)

        print("\nGetting contract decimals..")
        decimals = fundMe.getDecimals()
        print(decimals)

        print("\nGetting eth to dollars price..")
        dollar_amount = fundMe.getConversionRate(4)
        print(f"${float(dollar_amount)/float(decimals)}")

        print("\nFunding the contract")
        fundMe.fund({"from":account, "amount": 250000000000000000})
        print(f"{account}: {Web3.fromWei(fundMe.addressToAmountFunded(account), 'ether')}")
        print(Web3.fromWei(fundMe.balance(), 'ether'))

        print(f"\nWithdrawing funds.. Current funds in account: {Web3.fromWei(account.balance())}")
        fundMe.withdraw({"from":account})
        print(f"\nFunds withdrawn.. Current funds in account: {Web3.fromWei(account.balance())}")
        print(Web3.fromWei(fundMe.balance(), 'ether'))

