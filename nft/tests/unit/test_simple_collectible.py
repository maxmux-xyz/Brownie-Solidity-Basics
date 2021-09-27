from scripts.simple_collectible.deploy import (
    deploy_and_create,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONEMENTS
)
from brownie import network
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMENTS:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()