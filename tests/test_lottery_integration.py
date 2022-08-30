from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time
from brownie import network
import pytest


def test_can_pick_winner(lottery_contract):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({"from": account})
    # Two players
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    fund_with_link(lottery_contract)
    lottery_contract.endLottery({"from": account})
    # wait reaction from chain (rinkebey)
    time.sleep(180)
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0

# In terminal: brownie test -k test_can_pick_winner --network rinkeby -s
# brownie run scripts/deploy.py --network rinkeby = make it run on a real chain check etherscan
# Look at lottery deployed here, copy address go to rinkeby etherscan