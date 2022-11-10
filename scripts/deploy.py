from brownie import MerchantBuyer, accounts

def main():
    merchant = accounts[0]
    buyer = accounts[1]
    contract = MerchantBuyer.deploy(buyer,{'from':merchant})
    print(contract)