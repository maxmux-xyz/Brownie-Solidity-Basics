// SPDX-Licence_Identifier: MIT
pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

contract StorageFactory {

    SimpleStorage[] public simpleStorageArray;

    function CreateSimpleStorageContract() public {
        SimpleStorage _simpleStorage = new SimpleStorage();
        simpleStorageArray.push(_simpleStorage);
    }

    function SFStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // ADDRESS
        // ABI
        SimpleStorage _simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        _simpleStorage.setNumber(_simpleStorageNumber);
    }

    function SFGet(uint256 _simpleStorageIndex) public view returns(uint256) {
        SimpleStorage _simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        return _simpleStorage.getNumber();
    }
}