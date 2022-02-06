import imp
from brownie import FundMe
from scripts.utility import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"the current entry fee is {entrance_fee}")
    print("funding...")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    print(f"funded ${entrance_fee}!")


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print("withdrawing...")
    tx = fund_me.withdraw({"from": account})
    tx.wait(1)
    print("withdrawal complete!")


def main():
    fund()
    withdraw()
