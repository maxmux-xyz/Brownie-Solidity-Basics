from scripts.advanced_collectible.deploy import (
    deploy_and_create,
    get_contract,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONEMENTS
)
from brownie import network
import pytest
import time


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip("Only for integration testing.")
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(120)
    assert advanced_collectible.tokenCounter() == 1
