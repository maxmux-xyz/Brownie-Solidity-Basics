from brownie import (
    accounts,
    network,
    config,
    Contract,
    AdvancedCollectible,
    VRFCoordinatorMock,
    LinkToken
)
from web3 import Web3

FORKED_LOCAL_ENVIRONEMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONEMENTS = [
    'development', 'ganache-local',
    'hardhat', 'ganache', 'mainnet-fork'
]
OPENSEA_URL = 'https://testnets.opensea.io/assets/{address}/{token_id}'
sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
contract_to_mock = {
    "vrf": VRFCoordinatorMock,
    "link": LinkToken,
}
DECIMALS=8
INITIAL_VALUE=200000000000 # initial ethusd price is $2000


def main():
    deploy_and_create()

def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract('vrf'),
        get_contract('link'),
        config['networks'][network.show_active()]['keyHash'],
        config['networks'][network.show_active()]['fee'],
        {"from": account}
    )
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible(
        "None",
        {"from": account}
    )
    creating_tx.wait(1)
    print("NFT has been created!")
    return advanced_collectible, creating_tx


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(0.5, "ether")):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"Contract funded! {tx}")
    return tx


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
    link_token = LinkToken.deploy(
        {"from": account}
    )
    print("Deployed LinkToken")
    vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address,
        {"from": account}
    )
    print("Deployed VRFCoordinator")
