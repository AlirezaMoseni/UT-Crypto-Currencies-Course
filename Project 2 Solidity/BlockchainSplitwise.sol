// Please paste your contract's solidity code here
// Note that writing a contract here WILL NOT deploy it and allow you to access it from your client
// You should write and develop your contract in Remix and then, before submitting, copy and paste it here
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract Storage {

    
    address[] usersInThisDapp;
    mapping (address => bool) userIsAdded;
    mapping (address => mapping (address => uint32))  ledger;
    
    
     
    function lookup(address debtor, address creditor) public view returns (uint32 ret) {
        ret = ledger[debtor][creditor];
    }

    function add_IOU(address creditor, uint32 amount) public{
            require(amount>=0,"AMOUNT CANNOT BELOW ZERO");
            if(!userIsAdded[msg.sender]){
                usersInThisDapp.push(msg.sender);
                userIsAdded[msg.sender]=true;
            }
            if(!userIsAdded[creditor]){
                 usersInThisDapp.push(creditor);
                 userIsAdded[creditor]=true;
            }
            ledger[msg.sender][creditor] = amount;
    }
    
    function getAllUsers() public view returns(address[] memory users){
        users = usersInThisDapp;
    }
    
    function getDebtByUser(address user) public view returns(uint32 ret){
        uint totalUsers = usersInThisDapp.length;
        ret = 0;
        for (uint i=0;i<totalUsers;i++){
            ret = ret + ledger[user][usersInThisDapp[i]];
        }
    }
    
    
    function getDebtByUserToUser(address from,address to) public view returns(uint32 ret){
        ret = 0;
        ret = ledger[from][to];
    }
    
    
    function setDebtByUserToUser(address from,address to,uint32 amount) public {
     require(amount>=0,"AMOUNT CANNOT BELOW ZERO");
            if(!userIsAdded[from]){
                usersInThisDapp.push(from);
                userIsAdded[from]=true;
            }
            if(!userIsAdded[to]){
                 usersInThisDapp.push(to);
                 userIsAdded[to]=true;
            }
            ledger[from][to] = amount;
    }
    
    
}