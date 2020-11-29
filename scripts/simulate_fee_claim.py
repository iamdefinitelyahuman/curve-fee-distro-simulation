from brownie import chain, Contract

# the total accrued fee amount in USD
# you can get this from the main page of https://www.curve.fi
FEE_AMOUNT = 3_000_000

# the address you wish to check
ADDRESS_TO_CHECK = ""


def main():
    fee_token = Contract("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490")
    distributor = Contract("0xA464e6DCda8AC41e03616F95f4BC98a13b8922Dc")
    voting_escrow = Contract("0x5f3b5dfeb7b28cdbd7faba78963ee202a494e2a2")
    admin = distributor.admin()

    minter = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"
    fee_token.mint(distributor, FEE_AMOUNT * 10**18, {"from": minter})

    distributor.checkpoint_token({'from': admin})
    distributor.checkpoint_total_supply({'from': admin})
    chain.sleep(86400 * 14)
    distributor.checkpoint_token({'from': admin})
    distributor.checkpoint_total_supply({'from': admin})

    max_epoch = voting_escrow.user_point_epoch(ADDRESS_TO_CHECK)
    epoch = 0

    initial = fee_token.balanceOf(ADDRESS_TO_CHECK)
    while epoch < max_epoch:
        distributor.claim({'from': ADDRESS_TO_CHECK})
        epoch = distributor.user_epoch_of(ADDRESS_TO_CHECK)

    claimed = fee_token.balanceOf(ADDRESS_TO_CHECK) - initial

    print(f"Amount received: ${claimed/1e18:,.2f}")
