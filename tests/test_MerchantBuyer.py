from brownie import MerchantBuyer, accounts, exceptions
import pytest

def deploy():
    contract = MerchantBuyer.deploy(accounts[1],{"from":accounts[0]})
    return contract

def test_merchant_getter():
    contract = deploy()
    assert contract.Merchant() == accounts[0]
    pass

def test_buyer_getter():
    contract = deploy()
    assert contract.Buyer() == accounts[1]
    pass


# we will try to change price of product from buyer account, which should fail
def test_price_set_by_buyer_failure():
    contract = deploy()
    with pytest.raises(exceptions.VirtualMachineError):
        # setting price as 10ETH
        contract.createPrice(10**19,{"from":accounts[1]})
    pass


# we will try to change price of product from merchant account, which should succeed
def test_price_set_by_merchant_success():
    contract = deploy()
    # setting price as 10ETH
    contract.createPrice(10**19,{"from":accounts[0]})
    assert contract.Price() == 10**19
    pass


# we will only pay price of product without gas fee, which should fail
def test_payForProduct_less_payment_failure():
    contract = deploy()
    # setting price as 10ETH
    transaction = contract.createPrice(10**19,{"from":accounts[0]})
    transaction.wait(1)
    priceToPay = contract.Price()
    with pytest.raises(exceptions.VirtualMachineError):
        contract.payForProduct({"from":accounts[1],"value":priceToPay})
    pass


# we are paying price of product + gas fee, which should succeed
def test_payForProduct_enough_payment_success():
    contract = deploy()
    # setting price as 10ETH
    transaction = contract.createPrice(10**19,{"from":accounts[0]})
    transaction.wait(1)
    # price to pay is = price of product + gas fee 
    priceToPay = contract.Price() + 18*(10**10)
    contract.payForProduct({"from":accounts[1],"value":priceToPay})
    pass

def test_withdrawal():
    contract = deploy()
    previous_balance_of_merchant = accounts[0].balance()
    # setting price as 10ETH
    transaction = contract.createPrice(10**19,{"from":accounts[0]})
    transaction.wait(1)
    priceToPay = contract.Price() + 18*(10**10)
    transaction = contract.payForProduct({"from":accounts[1],"value":priceToPay})
    transaction.wait(1)
    transaction = contract.withdraw({"from":accounts[0]})
    transaction.wait(1)
    new_balance_of_merchant = accounts[0].balance()
    assert new_balance_of_merchant - previous_balance_of_merchant == priceToPay
    pass