from brownie import network, Lottery
import pytest
from scripts.deploy_lottery import deploy_lottery
from scripts.helpers import LOCAL_BLOCKHAIN_ENVIRONMENTS, fund_with_link, get_account
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(240)  # Have to wait a fair bit before vrf coordinator invokes callback

    winner = lottery.recentWinner()
    balance = lottery.balance()
    print(f"recent winner is {winner}")
    print(f"lottery address is {lottery.address}")
    print(f"account balance is {balance}")

    assert winner == account
    assert balance == 0
