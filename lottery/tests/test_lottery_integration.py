from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
import pytest
import time

from scripts.deploy import (
    deploy_lottery,
    get_contract,
    get_account,
    fund_with_link,
    INITIAL_VALUE,
    LOCAL_BLOCKCHAIN_ENVIRONEMENTS,
    FORKED_LOCAL_ENVIRONEMENTS
)

# Unit test is used to test small pieces of code independently: Dev Network
# Integration test is used to test across multiple complex systems: Testnet

def test_can_pick_winner():
    # if network.show_active() != 'rinkeby':
    #     pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()+1000})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()+1000})
    fund_with_link(lottery.address)
    lottery.endLottery({"from":account})
    time.sleep(120) # waiting for chainlink node to answer
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
