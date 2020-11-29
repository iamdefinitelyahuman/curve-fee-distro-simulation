from brownie import chain, Contract, ZERO_ADDRESS

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

    # mint or rug the distributor so it has exactly `FEE_AMOUNT`
    to_mint = FEE_AMOUNT * 10**10 - fee_token.balanceOf(distributor)
    if to_mint > 0:
        minter = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"
        fee_token.mint(distributor, to_mint, {"from": minter})
    elif to_mint < 0:
        fee_token.transfer(ZERO_ADDRESS, abs(to_mint), {'from': distributor})

    # checkpoint the supply and token
    distributor.checkpoint_token({'from': admin})
    distributor.checkpoint_total_supply({'from': admin})

    # sleep and checkpoint again, to ensure we also claim for the epoch where the tokens arrived
    chain.sleep(86400 * 14)
    distributor.checkpoint_token({'from': admin})
    distributor.checkpoint_total_supply({'from': admin})

    initial = fee_token.balanceOf(ADDRESS_TO_CHECK)
    max_epoch = voting_escrow.user_point_epoch(ADDRESS_TO_CHECK)
    epoch = 0

    # each call to claim advances the user epoch by a maximum of 50
    # if an account has increased or extended a lock many times,
    # it will have to make multiple claim transactions
    while epoch < max_epoch:
        distributor.claim({'from': ADDRESS_TO_CHECK})
        epoch = distributor.user_epoch_of(ADDRESS_TO_CHECK)

    claimed = fee_token.balanceOf(ADDRESS_TO_CHECK) - initial
    print(f"Amount received: ${claimed/1e18:,.2f}")
