from termcolor import cprint
from config import *
from main import *

if __name__ == "__main__":
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    eth_price = response.json()['ethereum']['usd']
    random.shuffle(KEYS_LIST)

    for privatekey in KEYS_LIST:

        choice = 1 # 0 - op | 1 - stg | 2 - both

        cprint(f'\n=============== start : {privatekey} ===============', 'white')

        if (choice != 1):
            AMOUNT_TO_SWAP = round(random.uniform(AMOUNT_FROM, AMOUNT_TO), 6) / eth_price

            uniswap_swap(privatekey, AMOUNT_TO_SWAP)
            sleeping(SLEEP_FROM, SLEEP_TO)
            delegate(privatekey)
            sleeping(SLEEP_FROM, SLEEP_TO)

        if(choice!=0):
            cprint(f'\n=============== stg delegation started ===============', 'white')
            network = 'ARBITRUM'
            web3 = Web3(Web3.HTTPProvider(RPC[network]))
            account = web3.eth.account.privateKeyToAccount(privatekey)
            my_address = account.address
            gas_price = web3.eth.gas_price
            chain_id = web3.eth.chain_id

            # 1) buying STG
            USDC_amount = random.uniform(AMOUNT_FROM, AMOUNT_TO)
            swap_out_str = 'USDC'
            swap_in_str = 'STG'

            state = inch_swap(web3, privatekey, network, swap_out_str, swap_in_str, my_address, USDC_amount)
            if not state:
                sys.exit(state)
            sleeping(SLEEP_FROM, SLEEP_TO)

            # 2) starting approve in a contract STG Token for veSTG
            aprove_adr_dict = {
                'to_ticker': 'STG',
                'to_adr': Web3.toChecksumAddress(network_erc20_addr[network]['STG']),
                'spender_ticker': 'veSTG',
                'spender_adr': Web3.toChecksumAddress(network_erc20_addr[network]['veSTG']),
            }
            approve_contract(web3, privatekey, network, aprove_adr_dict, my_address, gas_price)
            sleeping(SLEEP_FROM, SLEEP_TO)

            # 3) STG locking for 36 months, receiving veSTG
            STG_balance = get_token_balance(web3, network, swap_in_str, my_address)

            lock_STG(web3, privatekey, network, my_address, STG_balance)
            sleeping(SLEEP_FROM, SLEEP_TO)

            # 4) starting approve for USDC
            aprove_adr_dict = {
                'to_ticker': 'USDC',
                'to_adr': Web3.toChecksumAddress(network_erc20_addr[network]['USDC']),
                'spender_ticker': 'Stargate Finance: Router',
                'spender_adr': Web3.toChecksumAddress('0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614'),
            }
            approve_contract(web3, privatekey, network, aprove_adr_dict, my_address, gas_price)
            sleeping(SLEEP_FROM, SLEEP_TO)

            # 5) adding liquidity in USDC
            amount = random.uniform(AMOUNT_FROM, AMOUNT_TO) / 2
            add_liq_USDC(web3, privatekey, network, my_address, amount)
            sleeping(SLEEP_FROM, SLEEP_TO)

            # 6) approving S*USDC for Stargate Finance: LP Staking
            aprove_adr_dict = {
                'to_ticker': 'S*USDC',
                'to_adr': Web3.toChecksumAddress(network_erc20_addr[network]['SUSDC']),
                'spender_ticker': 'Stargate Finance: LP Staking',
                'spender_adr': Web3.toChecksumAddress('0xeA8DfEE1898a7e0a59f7527F076106d7e44c2176'),
            }
            approve_contract(web3, privatekey, network, aprove_adr_dict, my_address, gas_price)
            sleeping(SLEEP_FROM, SLEEP_TO)

            # 7) depositing into farm
            SUSDC_amount = get_token_balance(web3, network, 'SUSDC', my_address)
            deposit_farm(web3, privatekey, network, my_address, SUSDC_amount)

        sleeping(SLEEP_FROM, SLEEP_TO)
