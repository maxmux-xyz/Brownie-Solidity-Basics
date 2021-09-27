// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {

    address payable[] public players;
    uint256 public usdEntryFee;
    uint256 public randomness;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE { OPENED, CLOSED, CALCULATING_WINNER }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;
    address payable public recentWinner;
    event RequestedRandomness(bytes32 requestId);


    constructor(
        address _priceFeedAddress,
        address _addressVrfCoordinator,
        address _addressLinkToken,
        uint256 _fee,
        bytes32 _keyHash
        ) public
    VRFConsumerBase(_addressVrfCoordinator, _addressLinkToken) {
        usdEntryFee = 50 * (10 ** 18); // 50$ minimum
        // https://etherscan.io/address/0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        // 50$ minimum
        require(lottery_state == LOTTERY_STATE.OPENED, "Lottery needs to be opened");
        require(msg.value >= getEntranceFee(), "Not enough cash to enter the lottery!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256) {
        // We calculate how much is 50$ in ETH to get ethEntranceFee
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10; // Because it comes with only 8 decimals

        // $ usdEntryFee (10**(18*2=36)) | ?eth ethEntranceFee?
        // $ eth adjustedPrice (10**18)  | eth one (10**18)
        uint256 ethEntranceFee = (usdEntryFee * 10**18) / adjustedPrice; //To the power of 18
        return ethEntranceFee;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start new lottery. Currently open."
        );
        lottery_state = LOTTERY_STATE.OPENED;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        // Fetch a random number outside the blockchain using ChainlinkVRF
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't there yet");
        require(_randomness > 0, "Random not found");

        // Now we pick a random winner with a modulo function!
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        // Now we pay this winner
        recentWinner.transfer(address(this).balance);

        // Reset lottery
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}