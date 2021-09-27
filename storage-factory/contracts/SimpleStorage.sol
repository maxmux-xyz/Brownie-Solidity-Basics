// SPDX-Licence_Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 numberToStore;
    struct People {
        uint number;
        string name;
    }

    People[] public pple;
    mapping(string => uint256) public nameToFavNumber;

    function setNumber(uint256 _number) public {
        numberToStore = _number;
    }

    function getNumber() public view returns (uint256){
        return numberToStore;
    }

    function addPeople(uint _number, string memory _name) public {
        pple.push(People({name:_name, number:_number}));
        nameToFavNumber[_name] = _number;
    }
}