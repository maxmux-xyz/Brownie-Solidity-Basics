import time

from brownie import (
    config,
    network,
    Lottery,
    accounts,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface
)

FORKED_LOCAL_ENVIRONEMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONEMENTS = ['development', 'ganache-local']

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

DECIMALS=8
INITIAL_VALUE=200000000000 # initial ethusd price is $2000

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

def get_contract(contract_name):
    """Grab contract addresse from brownie config if defined.
    Otherwise it will deploy mock version of the contract.
    Return the mock contract.

    Args:
        contract_name: string
    Returns:
        The most recently deployed version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address,
            contract_type.abi)
    return contract

def deploy_mocks():
    account = get_account()
    mock_price_feed = MockV3Aggregator.deploy(
        DECIMALS,
        INITIAL_VALUE,
        {"from": account}
    )
    print("Deployed MockV3Aggregator")
    link_token = LinkToken.deploy(
        {"from": account}
    )
    print("Deployed LinkToken")
    vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address,
        {"from": account}
    )
    print("Deployed VRFCoordinatorMock")


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['keyHash'],
        {"from": account},
        publish_source=config['networks'][network.show_active()].get('verify', False),
    )
    print(f"Deployed Lottery contract: {lottery}")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    print(lottery)
    starting_tx = lottery.startLottery({'from': account})
    # starting_tx.wait(1)
    print("The lottery has started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    print(lottery)
    fee = lottery.getEntranceFee()
    entranceFee = fee + 100000
    # print(fee, entranceFee)
    # print(lottery.lottery_state())
    tx = lottery.enter({"from":account, "value":entranceFee})
    tx.wait(1)
    print("You entered the Lottery!")

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # Can also do with interfaces
    # link_token_contract = interface.LinkTokenContract(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"Contract funded! {tx}")
    return tx

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery()
    ending_transaction.wait(1)
    time.sleep(120)
    print(f"Lottery winner: {lottery.recentWinner()}")

def main():
    lottery = deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
