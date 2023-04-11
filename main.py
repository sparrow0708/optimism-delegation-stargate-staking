from web3 import Web3
from termcolor import cprint
import time
from config import *
import requests
import datetime
import json
import random
import sys

def uniswap_swap(privatekey, AMOUNT_TO_SWAP):
    try:

        web3 = Web3(Web3.HTTPProvider(RPC['OPTIMISM']))
        account = web3.eth.account.privateKeyToAccount(privatekey)
        address_wallet = account.address
        nonce = web3.eth.get_transaction_count(address_wallet)

        uniswap_contract = web3.eth.contract(address=web3.toChecksumAddress('0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45'), abi=ABI_UNISWAP) 

        from_token = '0x4200000000000000000000000000000000000006'
        to_token = '0x4200000000000000000000000000000000000042'

        value = intToDecimal(AMOUNT_TO_SWAP, 18) 

        data = uniswap_contract.encodeABI(fn_name="exactInputSingle", args=[(from_token, to_token, 500, address_wallet, value, 1455, 0)],)
        deadline = (int(time.time()) + 10000)
        multicall_function = uniswap_contract.get_function_by_selector("0x5ae401dc")

        contract_txn = {
            'chainId': web3.eth.chain_id, 
            'gas': random.randint(300000, 400000),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(address_wallet),
            'value': value,
            }

        transaction = multicall_function(deadline, [data]).build_transaction(contract_txn)

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=privatekey)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        cprint(f'\n>>> swap | https://optimistic.etherscan.io/tx/{web3.toHex(tx_token)}', 'green')

    except Exception as error:
        cprint(f'\n>>> swap | {address_wallet} | {error}', 'red')

def delegate(privatekey):
    try:

        web3 = Web3(Web3.HTTPProvider(RPC['OPTIMISM']))
        account = web3.eth.account.privateKeyToAccount(privatekey)
        address_wallet = account.address
        nonce = web3.eth.get_transaction_count(address_wallet)

        contractToken = '0x4200000000000000000000000000000000000042'
        contract = web3.eth.contract(address=contractToken, abi=ABI_DELEGATE)

        contract_txn = contract.functions.delegate(
            address_wallet
        ).build_transaction({
        'from': address_wallet,
        'gas': random.randint(300000, 400000),
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
        })
            
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=privatekey)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        cprint(f'>>> delegate | https://optimistic.etherscan.io/tx/{web3.toHex(tx_token)}', 'green')

    except Exception as error:
        cprint(f'>>> delegate | {address_wallet} | {error}', 'red')


def int_to_decimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))

def decimal_to_int(price, decimal):
    return price / int("".join((["1"] + ["0"] * decimal)))

def float_str(amount, decimals = 18):
    temp_str = "%0.18f"
    temp_str = temp_str.replace('18', str(decimals))
    text_float = temp_str % amount
    return text_float


def get_erc20_contract(web3, contract_address, ERC20_ABI=''):

    if ERC20_ABI == '':
        ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')

    contract = web3.eth.contract(Web3.toChecksumAddress(contract_address), abi=ERC20_ABI)

    return contract

def get_contract_balance(contract, user_address):

    contract_func = contract.functions

    symbol = contract_func.symbol().call()
    balance_wei = contract_func.balanceOf(user_address).call()  # in Wei
    token_decimals = contract_func.decimals().call()
    balance = balance_wei / 10 ** token_decimals
    #token_name = contract_func.name().call()
    #allowance = contract_func.allowance(some_contract_address, user_address).call()

    return {'symbol': symbol, 'balance': balance}

def get_token_balance(web3, network, ticker, my_address):
    contract = get_erc20_contract(web3, network_erc20_addr[network][ticker])
    balance_dict = get_contract_balance(contract, my_address)
    return balance_dict['balance']


def get_api_call_data(url):
    try:
        call_data = requests.get(url)
    except Exception as e:
        print(e)
        return get_api_call_data(url)
    try:
        api_data = call_data.json()
        return api_data
    except Exception as e:
        print(call_data.text)

def web_sushi(web3, private_key, network, contract, swap_out_str, swap_in_str, my_address, amount):
    try:
        now = datetime.datetime.now()
        now_dt = now.strftime("%d-%m-%Y %H:%M")
        swap_out_adr = Web3.toChecksumAddress(network_erc20_addr[network][swap_out_str])
        swap_in_adr = Web3.toChecksumAddress(network_erc20_addr[network][swap_in_str])
        swap_out_ABI = network_erc20_abi[network][swap_out_str]
        swap_out_contract = get_erc20_contract(web3, swap_out_adr, swap_out_ABI)
        out_decimals = swap_out_contract.functions.decimals().call()
        amount_d = int_to_decimal(amount, out_decimals)
        amount_str = float_str(amount)

        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(my_address)

        # if swap_out_str == 'ETH':
        #     func_sushi_swap = contract.functions.swapExactETHForTokens
        # else:
        #     func_sushi_swap = contract.functions.swapExactTokensForTokens

        contract_txn = contract.functions.swapExactETHForTokens(
        0, # amountOutMin здесь нужно высчитывать и ставить минимальное получаемое значение, на сумме больше 10$ могут боты отжать много, у меня с 1 транзы 30% отжали
        [swap_out_adr, swap_in_adr],
        my_address, # receiver
        (int(time.time()) + 10000) # deadline
        ).buildTransaction({
        'from': my_address,
        'value': amount_d,
        #'gas': gasLimit,
        'gasPrice': gas_price,
        'nonce': nonce,
        })

        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully swap {amount_str} {swap_out_str} on {swap_in_str} tx {txn_explorer[network]}{txn_text}", 'green')

    except Exception as error:
        cprint(f'\n{now_dt} {my_address} | Unsuccessfully swap {amount_str} {swap_out_str} on {swap_in_str} | {error}', 'red')

def api_1inch_is_stable():
    _1inchurl = f'{base_url}/healthcheck'
    json_data = get_api_call_data(_1inchurl)

    if json_data['status'] == 'OK':
        return True

    cprint(f'\nAPI 1inch not available! No further work possible', 'red')
    return False

def inch_swap(web3, private_key, network, swap_out_str, swap_in_str, my_address, amount):

    if not api_1inch_is_stable():
        return 1

    now = datetime.datetime.now()
    now_dt = now.strftime("%d-%m-%Y %H:%M")

    try:
        # swap_out = Web3.toChecksumAddress("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")  # native ETH in network
        swap_out_adr = Web3.toChecksumAddress(network_erc20_addr[network][swap_out_str])
        swap_out_ABI = network_erc20_abi[network][swap_out_str]
        swap_out_contract = get_erc20_contract(web3, swap_out_adr, swap_out_ABI)
        out_decimals = swap_out_contract.functions.decimals().call()
        amount_d = int_to_decimal(amount, out_decimals)
        amount_str = float_str(amount, out_decimals)
        slippage = '0.5'

        out_allowance = inch_allowance(swap_out_adr, my_address)

        swap_in_adr = Web3.toChecksumAddress(network_erc20_addr[network][swap_in_str])
        # swap_in_ABI = network_erc20_abi[network][swap_in_str]
        # swap_out_contract = get_erc20_contract(web3, swap_in_adr, swap_in_ABI)

        if int(out_allowance) <= amount_d:
            state = inch_set_approve(web3, private_key, network, swap_out_adr, my_address)
            if not state:
                return state
            else:
                time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))

        _1inchurl = f'{base_url}/swap?fromTokenAddress={swap_out_adr}&toTokenAddress={swap_in_adr}&amount={amount_d}&fromAddress={my_address}&slippage={slippage}'
        json_data = get_api_call_data(_1inchurl)

        tx = json_data['tx']
        tx['nonce'] = web3.eth.get_transaction_count(my_address)
        tx['to'] = Web3.toChecksumAddress(tx['to'])
        tx['gasPrice'] = int(tx['gasPrice'])
        tx['value'] = int(tx['value'])
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_text = tx_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully swap {amount_str} {swap_out_str} on {swap_in_str} tx {txn_explorer[network]}{txn_text}", 'green')
        return True

    except Exception as e:
        error_str = f'\n{now_dt} {my_address} | Unsuccessfully swap {amount_str} {swap_out_str} on {swap_in_str} | {e}'
        if 'description' in json_data.keys():
            error_des = json_data['description']
            error_str += f'| {error_des}'

        cprint(error_str, 'red')
        return False

def inch_set_approve(web3, private_key, network, swap_out_str, my_address):

    now = datetime.datetime.now()
    now_dt = now.strftime("%d-%m-%Y %H:%M")

    try:
        _1inchurl = f'{base_url}/approve/transaction?tokenAddress={swap_out_str}'
        tx = get_api_call_data(_1inchurl)

        tx['gasPrice'] = int(tx['gasPrice'])
        tx['from'] = Web3.toChecksumAddress(my_address)
        tx['to'] = Web3.toChecksumAddress(tx['to'])
        tx['value'] = int(tx['value'])
        tx['nonce'] = web3.eth.get_transaction_count(my_address)

        estimate = web3.eth.estimate_gas(tx)
        gas_limit = estimate
        # gas_limit = int(estimate + estimate * 0.25)
        tx['gas'] = gas_limit

        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_text = tx_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully approved on 1inch {swap_out_str} tx {txn_explorer[network]}{txn_text}", 'green')
        return True

    except Exception as e:
        error_str = f'\n{now_dt} {my_address} | Unsuccessfully approved on 1inch {swap_out_str} | {e}'
        if 'description' in tx.keys():
            error_des = tx['description']
            error_str += f'| {error_des}'

        cprint(error_str, 'red')
        return False

def inch_allowance(swap_out_adr, my_address):
    _1inchurl = f'{base_url}/approve/allowance?tokenAddress={swap_out_adr}&walletAddress={my_address}'
    json_data = get_api_call_data(_1inchurl)
    out_allowance = None

    if 'allowance' in json_data.keys():
        out_allowance = json_data['allowance']

    return out_allowance


def approve_contract(web3, private_key, network, adr_dict, my_address, gas_price):
    try:
        approve_amount = 2 ** 256 - 1
        now = datetime.datetime.now()
        now_dt = now.strftime("%d-%m-%Y %H:%M")

        contract = get_erc20_contract(web3, adr_dict['to_adr'])
        allowance = contract.functions.allowance(my_address, adr_dict['spender_adr']).call()

        if allowance == approve_amount:
            return True

        contract_txn = contract.functions.approve(adr_dict['spender_adr'], approve_amount).buildTransaction({
            'from': my_address,
            'value': 0,
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(my_address),
            })

        estimate = web3.eth.estimate_gas(contract_txn)
        gas_limit = estimate
        # gas_limit = int(estimate + estimate * 0.25)
        contract_txn['gas'] = gas_limit

        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully approved {adr_dict['to_ticker']} for {adr_dict['spender_ticker']} tx {txn_explorer[network]}{txn_text}",'green')
        return True

    except Exception as error:
        cprint(f"\n{now_dt} {my_address} | Unsuccessfully approved {adr_dict['to_ticker']} for {adr_dict['spender_ticker']} | {error}", 'red')
        return False


def lock_STG(web3, private_key, network, my_address, amount):
    try:
        now = datetime.datetime.now()
        now_dt = now.strftime("%d-%m-%Y %H:%M")

        contr_addr = Web3.toChecksumAddress(network_erc20_addr[network]['veSTG'])
        contr_addr_ABI = network_erc20_abi[network]['veSTG']
        contr = get_erc20_contract(web3, contr_addr, contr_addr_ABI)
        out_decimals = contr.functions.decimals().call()
        amount_d = int_to_decimal(amount, out_decimals)
        amount_str = float_str(amount)
        time = 1764201600 # 36 months

        contract_txn = contr.functions.create_lock(amount_d, time).buildTransaction({
            'from': my_address,
            'value': 0,
            #'gas': gasLimit,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(my_address),
            })

        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully locked {amount_str} STG tx {txn_explorer[network]}{txn_text}", 'green')

    except Exception as error:
        cprint(f'\n{now_dt} {my_address} | Unsuccessfully locked {amount_str} STG | {error}', 'red')

def add_liq_USDC(web3, private_key, network, my_address, amount):
    try:
        now = datetime.datetime.now()
        now_dt = now.strftime("%d-%m-%Y %H:%M")

        contr_addr = Web3.toChecksumAddress('0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614') # Stargate Finance: Router
        contr_ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountLD","type":"uint256"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"bytes","name":"payload","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"reason","type":"bytes"}],"name":"CachedSwapSaved","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"srcChainId","type":"uint16"},{"indexed":true,"internalType":"bytes","name":"srcAddress","type":"bytes"},{"indexed":true,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"srcPoolId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"dstPoolId","type":"uint256"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountSD","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"mintAmountSD","type":"uint256"}],"name":"RedeemLocalCallback","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"bridgeFunctionType","type":"uint8"},{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"Revert","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"srcChainId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"to","type":"bytes"},{"indexed":false,"internalType":"uint256","name":"redeemAmountSD","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"mintAmountSD","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":true,"internalType":"bytes","name":"srcAddress","type":"bytes"}],"name":"RevertRedeemLocal","type":"event"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"}],"name":"activateChainPath","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"uint256","name":"_amountLD","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"addLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"bridge","outputs":[{"internalType":"contract Bridge","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"cachedSwapLookup","outputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"payload","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"bool","name":"_fullMode","type":"bool"}],"name":"callDelta","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint256","name":"_nonce","type":"uint256"}],"name":"clearCachedSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"uint256","name":"_weight","type":"uint256"}],"name":"createChainPath","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint8","name":"_sharedDecimals","type":"uint8"},{"internalType":"uint8","name":"_localDecimals","type":"uint8"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"}],"name":"createPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"components":[{"internalType":"uint256","name":"credits","type":"uint256"},{"internalType":"uint256","name":"idealBalance","type":"uint256"}],"internalType":"struct Pool.CreditObj","name":"_c","type":"tuple"}],"name":"creditChainPath","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"contract Factory","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcPoolId","type":"uint16"},{"internalType":"uint256","name":"_amountLP","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"instantRedeemLocal","outputs":[{"internalType":"uint256","name":"amountSD","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintFeeOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeeOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint8","name":"_functionType","type":"uint8"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"bytes","name":"_transferAndCallPayload","type":"bytes"},{"components":[{"internalType":"uint256","name":"dstGasForCall","type":"uint256"},{"internalType":"uint256","name":"dstNativeAmount","type":"uint256"},{"internalType":"bytes","name":"dstNativeAddr","type":"bytes"}],"internalType":"struct IStargateRouter.lzTxObj","name":"_lzTxParams","type":"tuple"}],"name":"quoteLayerZeroFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"uint256","name":"_amountLP","type":"uint256"},{"internalType":"bytes","name":"_to","type":"bytes"},{"components":[{"internalType":"uint256","name":"dstGasForCall","type":"uint256"},{"internalType":"uint256","name":"dstNativeAmount","type":"uint256"},{"internalType":"bytes","name":"dstNativeAddr","type":"bytes"}],"internalType":"struct IStargateRouter.lzTxObj","name":"_lzTxParams","type":"tuple"}],"name":"redeemLocal","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint256","name":"_nonce","type":"uint256"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amountSD","type":"uint256"},{"internalType":"uint256","name":"_mintAmountSD","type":"uint256"}],"name":"redeemLocalCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint256","name":"_nonce","type":"uint256"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"uint256","name":"_amountSD","type":"uint256"},{"internalType":"bytes","name":"_to","type":"bytes"}],"name":"redeemLocalCheckOnRemote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"uint256","name":"_amountLP","type":"uint256"},{"internalType":"uint256","name":"_minAmountLD","type":"uint256"},{"internalType":"bytes","name":"_to","type":"bytes"},{"components":[{"internalType":"uint256","name":"dstGasForCall","type":"uint256"},{"internalType":"uint256","name":"dstNativeAmount","type":"uint256"},{"internalType":"bytes","name":"dstNativeAddr","type":"bytes"}],"internalType":"struct IStargateRouter.lzTxObj","name":"_lzTxParams","type":"tuple"}],"name":"redeemRemote","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint256","name":"_nonce","type":"uint256"}],"name":"retryRevert","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"revertLookup","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint256","name":"_nonce","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"components":[{"internalType":"uint256","name":"dstGasForCall","type":"uint256"},{"internalType":"uint256","name":"dstNativeAmount","type":"uint256"},{"internalType":"bytes","name":"dstNativeAddr","type":"bytes"}],"internalType":"struct IStargateRouter.lzTxObj","name":"_lzTxParams","type":"tuple"}],"name":"revertRedeemLocal","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"}],"name":"sendCredits","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract Bridge","name":"_bridge","type":"address"},{"internalType":"contract Factory","name":"_factory","type":"address"}],"name":"setBridgeAndFactory","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"bool","name":"_batched","type":"bool"},{"internalType":"uint256","name":"_swapDeltaBP","type":"uint256"},{"internalType":"uint256","name":"_lpDeltaBP","type":"uint256"},{"internalType":"bool","name":"_defaultSwapMode","type":"bool"},{"internalType":"bool","name":"_defaultLPMode","type":"bool"}],"name":"setDeltaParam","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"address","name":"_feeLibraryAddr","type":"address"}],"name":"setFeeLibrary","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"uint256","name":"_mintFeeBP","type":"uint256"}],"name":"setFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setMintFeeOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setProtocolFeeOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"bool","name":"_swapStop","type":"bool"}],"name":"setSwapStop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"uint16","name":"_weight","type":"uint16"}],"name":"setWeightForChainPath","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"uint256","name":"_amountLD","type":"uint256"},{"internalType":"uint256","name":"_minAmountLD","type":"uint256"},{"components":[{"internalType":"uint256","name":"dstGasForCall","type":"uint256"},{"internalType":"uint256","name":"dstNativeAmount","type":"uint256"},{"internalType":"bytes","name":"dstNativeAddr","type":"bytes"}],"internalType":"struct IStargateRouter.lzTxObj","name":"_lzTxParams","type":"tuple"},{"internalType":"bytes","name":"_to","type":"bytes"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"swap","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint256","name":"_nonce","type":"uint256"},{"internalType":"uint256","name":"_srcPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstPoolId","type":"uint256"},{"internalType":"uint256","name":"_dstGasForCall","type":"uint256"},{"internalType":"address","name":"_to","type":"address"},{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"eqFee","type":"uint256"},{"internalType":"uint256","name":"eqReward","type":"uint256"},{"internalType":"uint256","name":"lpFee","type":"uint256"},{"internalType":"uint256","name":"protocolFee","type":"uint256"},{"internalType":"uint256","name":"lkbRemove","type":"uint256"}],"internalType":"struct Pool.SwapObj","name":"_s","type":"tuple"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"swapRemote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"withdrawMintFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_poolId","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"withdrawProtocolFee","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        contr = get_erc20_contract(web3, contr_addr, contr_ABI)
        decimal = 6 # будет разный от суммы, в нашем случае для х.хх
        amount_d = int_to_decimal(amount, decimal)
        amount_str = float_str(amount, decimal)
        pool_id = 1

        contract_txn = contr.functions.addLiquidity(pool_id, amount_d, my_address).buildTransaction({
            'from': my_address,
            'value': 0,
            #'gas': gasLimit,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(my_address),
            })

        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully add_liq_USDC {amount_str} tx {txn_explorer[network]}{txn_text}", 'green')
    except Exception as error:
        cprint(f'\n{now_dt} {my_address} | Unsuccessfully add_liq_USDC {amount_str} | {error}', 'red')

def deposit_farm(web3, private_key, network, my_address, amount):
    try:
        now = datetime.datetime.now()
        now_dt = now.strftime("%d-%m-%Y %H:%M")

        contr_addr = Web3.toChecksumAddress('0xea8dfee1898a7e0a59f7527f076106d7e44c2176') # Stargate Finance: LP Staking
        contr_ABI = '[{"inputs":[{"internalType":"contract StargateToken","name":"_stargate","type":"address"},{"internalType":"uint256","name":"_stargatePerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"BONUS_MULTIPLIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IERC20","name":"_lpToken","type":"address"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lpBalances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingStargate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IERC20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accStargatePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_stargatePerBlock","type":"uint256"}],"name":"setStargatePerBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stargate","outputs":[{"internalType":"contract StargateToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stargatePerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        contr = get_erc20_contract(web3, contr_addr, contr_ABI)
        decimal = 6
        amount_d = int_to_decimal(amount, decimal) # S*USDC
        amount_str = float_str(amount, decimal)

        contract_txn = contr.functions.deposit(0, amount_d).buildTransaction({
            'from': my_address,
            'value': 0,
            #'gas': gasLimit,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(my_address),
            })

        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        cprint(f"\n{now_dt} {my_address} | Successfully deposit Stargate Finance: LP Staking {amount_str} S*USDC tx {txn_explorer[network]}{txn_text}", 'green')

    except Exception as error:
        cprint(f'\n{now_dt} {my_address} | Unsuccessfully deposit Stargate Finance: LP Staking {amount_str} S*USDC | {error}', 'red')

