// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22;

contract MerchantBuyer {
    address public Merchant;
    address public Buyer;
    uint public Price;

    constructor(address buyer) {
        Merchant = msg.sender;
        Buyer = buyer;
    }
 
    function createPrice(uint price) public {
        require(msg.sender == Merchant,"You must be Merchant to change price");
        Price = price;
    }

    function payForProduct() public payable {
        // gas Fee for one operation is around 90000000000, so I used 2 times of it to make sure that merchant doesn't lose money
        uint gasFee = 180000000000;
        require(msg.value >= gasFee + Price, "Insufficient money transfered");
    }

    function withdraw() public {
        require(msg.sender == Merchant,"You must be Merchant to withdraw funds");
        payable(Merchant).transfer(address(this).balance);
    }
}