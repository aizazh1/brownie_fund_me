// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    address[] public funders;
    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        uint256 minUSD = 5 * 10**18; //convert to wei, 10**8 for gwei

        require(
            getConversionRate(msg.value) >= minUSD,
            "You need to spend more eth!"
        );

        addressToAmountFunded[msg.sender] += msg.value;

        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10); //convert to wei
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        return (ethPrice * ethAmount) / (10**18); //convert from wei to eth
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 5 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 10**18;
        return (minimumUSD * precision) / price;
    }

    function getFunding() public view returns (uint256) {
        return address(this).balance;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner!");
        _;
    }

    function withdraw() public payable onlyOwner {
        require(getFunding() > 0, "Contract has no balance!");

        msg.sender.transfer(getFunding());

        for (uint256 i = 0; i < funders.length; i++) {
            addressToAmountFunded[funders[i]] = 0;
        }

        funders = new address[](0);
    }
}
