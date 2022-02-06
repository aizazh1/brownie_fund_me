import pytest
from scripts.utility import get_account, LOCAL_BLOCKHAIN_ENVIRONMENTS
from scripts.deploy import deploy
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy()
    other_account = accounts[-1]
    tx = fund_me.fund({"from": other_account, "value": fund_me.getEntranceFee()})
    tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": other_account})
