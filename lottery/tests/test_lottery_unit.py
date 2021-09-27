from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
import pytest

from scripts.deploy import (
    deploy_lottery,
    get_contract,
    get_account,
    fund_with_link,
    INITIAL_VALUE,
    LOCAL_BLOCKCHAIN_ENVIRONEMENTS
)

# Unit test is used to test small pieces of code independently: Dev Network
# Integration test is used to test across multiple complex systems: Testnet

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # 2,000 eth / usd
    # 50 / 2000 = 0.025 (because INITIAL_VALUE=200000000000)
    expected_entrance_fee_ether = 50 / (INITIAL_VALUE/10**8) # 0.025
    expected_entrance_fee = Web3.toWei(expected_entrance_fee_ether, 'ether')
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee

def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state() == 2

def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from":account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)

    starting_balance_account = account.balance()
    peak_lottery_balance_account = lottery.balance()

    transaction = lottery.endLottery({"from":account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]

    # Now we pretend to be the chainlink node and get the random number!
    # In dev mode this never happens because we are not connected to any cainlink nodes!
    randomNumber = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, randomNumber, lottery.address,
        {"from":account}
        )
    # 777 % 3 = 0, therefore account wins

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == peak_lottery_balance_account + starting_balance_account
