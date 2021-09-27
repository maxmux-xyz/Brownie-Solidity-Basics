from scripts.advanced_collectible.deploy import (
    deploy_and_create,
    get_contract,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONEMENTS
)
from brownie import network
import pytest


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    advanced_collectible, creating_tx = deploy_and_create()
    # Use the creation transaction to get request
    request_id = creating_tx.events['requestedCollectible']['requestId']
    random_number = 777
    get_contract('vrf').callBackWithRandomness(
        request_id,
        random_number, # Faking that chainlink is returning 777 random number
        advanced_collectible.address,
        {"from":get_account()}
    )
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
