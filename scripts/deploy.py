from brownie import FundMe, MockV3Aggregator, network, config
from scripts.utility import get_account, deploy_mocks, LOCAL_BLOCKHAIN_ENVIRONMENTS


def deploy():
    account = get_account()
    print(f"the active network is {network.show_active()}")

    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    return fund_me


def main():
    deploy()
