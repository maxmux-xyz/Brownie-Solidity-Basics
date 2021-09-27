from brownie import accounts, network, config, SimpleCollectible

FORKED_LOCAL_ENVIRONEMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONEMENTS = [
    'development', 'ganache-local',
    'hardhat', 'ganache', 'mainnet-fork'
]
OPENSEA_URL = 'https://testnets.opensea.io/assets/{address}/{token_id}'
sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def main():
    deploy_and_create()

def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri)
    tx.wait(1)
    print(tx)
    nft_url = OPENSEA_URL.format(
        address = simple_collectible.address,
        token_id = simple_collectible.tokenCounter() - 1
    )
    print(f"NFT deployed! View at {nft_url}")
    return simple_collectible


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
