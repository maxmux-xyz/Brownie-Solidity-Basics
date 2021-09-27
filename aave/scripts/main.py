from brownie import accounts, network, config, interface
from web3 import Web3

import time

FORKED_LOCAL_ENVIRONEMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONEMENTS = [
    'development',
    'local-ganache',
    'ganache',
    'mainnet-fork'
]
# 0.1
AMOUNT = Web3.toWei(0.1, 'ether') # 100000000000000000 Wei

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

def get_weth():
    """Swap ETH with WETH. We need to connect to a WETH contract.
    1. ABI
    2. Address
    For that we will use an interface.
    """
    account = get_account()
    weth = interface.IWeth(config['networks'][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value":0.1*10**18})
    tx.wait(1)
    print(f"Received 0.1 WETH")

def borrow():
    account = get_account()
    erc20_address = config['networks'][network.show_active()]["weth_token"]

def get_lending_pool():
    # There is a contract telling where the lending contract is
    # We get ABI and address of that contract here
    # We grab it's interface
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config['networks'][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_addresses = lending_pool_addresses_provider.getLendingPool()
    # Now we have address, we need ABI
    lending_pool = interface.ILendingPool(lending_pool_addresses)
    return lending_pool

def approve_erc20_token(amount, spender_address, erc20_address, account):
    # Need ABI and address of the contract
    print("Approving ERC20Token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender_address, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return True

def get_borrowable_date(lending_pool, account):
    print("Getting user accoutn data")
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor
    ) = lending_pool.getUserAccountData(account)
    total_collateral_eth = Web3.fromWei(totalCollateralETH, 'ether')
    total_debt_eth = Web3.fromWei(totalDebtETH, 'ether')
    available_borrows_eth = Web3.fromWei(availableBorrowsETH, 'ether')
    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrows_eth} worth of ETH")
    print("Done")
    return (float(available_borrows_eth), float(total_debt_eth))

def get_address_price(price_feed_address, ticker):
    print(f"Getting Price Data: {ticker}")

    price_feed_contract = interface.IAggregatorV3(price_feed_address)
    (
        roundId,
        answer,
        startedAt,
        updatedAt,
        answeredInRound
    ) = price_feed_contract.latestRoundData()
    price = Web3.fromWei(answer, 'ether')
    print(f"{ticker}: {price}")
    return float(price)

def repay_all(amount, lending_pool, asset_address, account):
    """REpay the borrowed money

    Args:
        asset ETH address: Contract address of the ERC20 token borrowed
        amount float: amount to repay

    """
    print("Approving the asset transfer.")
    approve_erc20_token(
        Web3.toWei(amount, 'ether'),
        lending_pool,
        asset_address,
        account
    )

    print("Repaying the asset {}")
    repay_tx = lending_pool.repay(
        asset_address,
        amount,
        1, # 0: Variable ; 1: Stable
        account.address,
        {"from":account}
    )
    repay_tx.wait(1)
    print("Repayed!")

def main():
    account = get_account()
    erc20_address = config['networks'][network.show_active()]["weth_token"]
    # 1. Swap ETH with WETH
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # 2. Deposit some ETH into Aave
    # ABI and address of aave contract
    lending_pool = get_lending_pool()
    print(lending_pool)

    # Take the WETH and deposit it in the contract
    # WE need to approve it first
    approve_erc20_token(AMOUNT, lending_pool.address, erc20_address, account)

    # Deposit function
    # address asset, uint256 amount, address onBehalfOf, uint16 referralCode
    # referralCode is deprecated, always 0
    print("Depositing")
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0,
        {"from":account}
    )
    tx.wait(1)
    print("Deposited")

    # 3. Borrow some asset with ETH collateral
    # Now we can borrow another asset!! But how much? We do we have and what can we borrow?
    # getUserAccountData!
    available_borrows_eth, total_debt_eth = get_borrowable_date(lending_pool, account)
    # Now we can borrow some DAI! We know how much ETH we can borrow (available_borrows_eth)
    # But how much DAI is that? Use chainlink price feed!
    dai_eth_price_feed = config['networks'][network.show_active()]["dai_eth_price_feed"]
    dai_eth_price = get_address_price(dai_eth_price_feed, 'dai/eth')

    # calculate amount of math we can borrow!
    amount_of_dai_possible_to_borrow = (1 / dai_eth_price) * (available_borrows_eth * 0.95)
    print(f"We are going to borrow: {amount_of_dai_possible_to_borrow} DAI")
    dai_address = config['networks'][network.show_active()]['dai_token']
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_of_dai_possible_to_borrow, 'ether'),
        1, # Variable or stable APY? stable is 1 variable is 0
        0, # Deprecated
        account.address, # On belhaf of ourself!
        {"from": account}
    )
    borrow_tx.wait(1)
    print("borrowed some DAI!")
    available_borrows_eth, total_debt_eth = get_borrowable_date(lending_pool, account)

    # 4. Repay everything back
    repay_all(
        AMOUNT,
        lending_pool,
        config['networks'][network.show_active()]['dai_token'],
        account
    )
    time.sleep(60)
    available_borrows_eth, total_debt_eth = get_borrowable_date(lending_pool, account)

