pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract MyToken is ERC20 {

    constructor(uint256 initialSupply) ERC20('MaximeToken', 'MTK') {
        _mint(msg.sender, initialSupply);
    }

}