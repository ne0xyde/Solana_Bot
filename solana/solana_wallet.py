import aiohttp
from decouple import config
from db_handler.db_funk import get_solana_address

HEADERS = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": f"{config('TATUM_API-KEY')}"
    }


async def create_solana_wallet():
    url = "https://api.tatum.io/v3/solana/wallet"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                mnemonic = data.get("mnemonic")
                address = data.get("address")
                private_key = data.get("privateKey")
                return mnemonic, address, private_key
            else:
                raise Exception(f"API Error: {response.text()} \n{await response.text()}")


async def get_solana_balance(solana_address: str):
    url = f"https://api.tatum.io/v3/solana/account/balance/{solana_address}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                balance = data.get("balance")
                return balance
            else:
                raise Exception(f"API Error: {response.text()} \n{await response.text()}")


async def send_solana_to_wallet(user_id: int, solana_target_address: str, solana_value: int or float):
    url = "https://api.tatum.io/v3/solana/transaction"
    solana_address, private_key = await get_solana_address(user_id=user_id, private=True)
    payload = {
        "from": solana_address,
        "to": solana_target_address,
        "amount": str(solana_value),
        "fromPrivateKey": private_key,
        "feePayer": solana_address,
        "feePayerPrivateKey": private_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=HEADERS) as response:
            print(f'status = {response.status}')
            if response.status == 200:
                data = await response.json()
                tx_id = data.get("txId")
                return tx_id
            else:
                print(f"API Error: {response.status} \n{await response.text()}")
                a = await response.json()
                return a['cause']
