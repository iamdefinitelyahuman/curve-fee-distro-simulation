# curve-fee-distro-simulation
Simulation to check the size of your historic fee distribution claim.

## Installation and Setup

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already.

2. Sign up for [Infura](https://infura.io/) and generate an API key. Store it in the `WEB3_INFURA_PROJECT_ID` environment variable.

```bash
export WEB3_INFURA_PROJECT_ID=YourProjectID
```

3. Sign up for [Etherscan](www.etherscan.io) and generate an API key. This is required for fetching source codes of the mainnet contracts we will be interacting with. Store the API key in the `ETHERSCAN_TOKEN` environment variable.

```bash
export ETHERSCAN_TOKEN=YourApiToken
```

4. Clone this repository.

```bash
git clone https://github.com/iamdefinitelyahuman/curve-fee-distro-simulation.git
```

## Usage

To check your historic fee claim amount:

1. Open [`scripts/simulate_fee_claim.py`](scripts/simulate_fee_claim.py). Modify the `FEE_AMOUNT` and `ADDRESS_TO_CHECK` variables.

2. Run the script:

```bash
brownie run simulate_fee_claim
```

## License

This project is licensed under the [MIT license](LICENSE).

