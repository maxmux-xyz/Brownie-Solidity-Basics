1. Users can enter the lottery with ETH based on a USD fee
2. An admin will choose when the lotterty is over
3. Lottery will pick a random winner

How do we test this?

#### 1. `mainnet-fork`
- `brownie networks delete mainnet-fork`
- `brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/qtoDAV-MlWCnezxI6sISm8Xp-jo8nmNT accounts=10 mnemonic=brownie port=8545`
- `brownie test --network mainnet-fork`

#### 2. `development` with `mocks`
#### 3. `testnet`