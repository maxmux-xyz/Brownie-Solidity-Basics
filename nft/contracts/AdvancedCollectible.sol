// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter = 0;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);
    event randomNumberReturned(uint256 indexed tokenId, uint256 randomnNumber);

    constructor(
        address _VRFCoordinatorAddress,
        address _LinkTokenAddress,
        bytes32 _keyhash, uint256 _fee) public
    ERC721('DoggieCoin', 'DOC')
    VRFConsumerBase(_VRFCoordinatorAddress, _LinkTokenAddress) {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible(string memory tokenURI) public {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectible(requestId, msg.sender);
    }

    /**
     * Callback function used by VRF Coordinator
     */
    function fulfillRandomness(bytes32 requestId, uint256 randomnNumber) internal override {
        address dogOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];

        uint256 NewTokenId = tokenCounter;

        _safeMint(dogOwner, NewTokenId);
        _setTokenURI(NewTokenId, tokenURI);

        Breed breed = Breed(randomnNumber % 3);
        tokenIdToBreed[NewTokenId] = breed;
        requestIdToTokenId[requestId] = NewTokenId;

        emit randomNumberReturned(NewTokenId, randomnNumber);
        emit breedAssigned(NewTokenId, breed);

        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // Three token
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}