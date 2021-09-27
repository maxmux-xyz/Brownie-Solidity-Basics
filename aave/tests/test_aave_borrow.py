from scripts.main import (
    get_address_price,
    get_lending_pool,
    approve_erc20_token,
    get_account,
)
from brownie import config, network


def test_get_asset_price():
    # Arrange / Act
    asset_price = get_address_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"],
        'dai/eth'
    )
    # Assert
    assert asset_price > 0


def test_get_lending_pool():
    # Arrange / Act
    lending_pool = get_lending_pool()
    # Assert
    assert lending_pool != None


def test_approve_erc20():
    # Arrange
    account = get_account()
    lending_pool = get_lending_pool()
    amount = 1000000000000000000  # 1
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    # Act
    approved = approve_erc20_token(amount, lending_pool.address, erc20_address, account)
    # Assert
    assert approved is True
