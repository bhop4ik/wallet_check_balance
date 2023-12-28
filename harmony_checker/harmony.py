import aiohttp
import asyncio
import csv

# Harmony blockchain explorer API endpoint
endpoint = "https://api.s0.t.hmny.io/"

async def get_balance(session, address):
    params = {
        "jsonrpc": "2.0",
        "method": "hmy_getBalance",
        "params": [address, "latest"],
        "id": 1,
    }
    async with session.post(endpoint, json=params) as response:
        if response.status == 200:
            result = await response.json()
            if 'result' in result:
                balance = int(result['result'], 16) / 1e18
                return balance
            else:
                print(f"Error: 'result' not found in the response for address {address}")
        else:
            print(f"Failed to fetch balance for address {address}, HTTP status code: {response.status}")
        return None

async def get_transaction_count(session, address):
    params = {
        "jsonrpc": "2.0",
        "method": "hmy_getTransactionCount",
        "params": [address, "latest"],
        "id": 1,
    }
    async with session.post(endpoint, json=params) as response:
        if response.status == 200:
            result = await response.json()
            if 'result' in result:
                transaction_count = int(result['result'], 16)
                return transaction_count
            else:
                print(f"Error: 'result' not found in the response for address {address}")
        else:
            print(f"Failed to fetch transaction count for address {address}, HTTP status code: {response.status}")
        return None

async def write_wallet_data(wallet_addresses):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for address in wallet_addresses:
            tasks.append(asyncio.create_task(get_balance(session, address)))
            tasks.append(asyncio.create_task(get_transaction_count(session, address)))

        results = await asyncio.gather(*tasks)

        with open('harmony_wallets.csv', 'w', newline='') as csvfile:
            fieldnames = ['Wallet', 'Address', 'Balance', 'Transaction Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, address in enumerate(wallet_addresses, 1):
                balance = results[(i-1)*2]
                transaction_count = results[((i-1)*2)+1]
                
                if balance is not None and transaction_count is not None:
                    wallet_label = f"{i}st Wallet" if i == 1 else f"{i}nd Wallet" if i == 2 else f"{i}rd Wallet" if i == 3 else f"{i}th Wallet"
                    writer.writerow({'Wallet': wallet_label, 'Address': address, 'Balance': balance, 'Transaction Count': transaction_count})

# Read wallet addresses from wallet.txt file
with open('wallet.txt', 'r') as file:
    wallet_addresses = [line.strip() for line in file]

# Starts the asynchronous loop
asyncio.run(write_wallet_data(wallet_addresses))

print("Finished writing balances and transaction counts to harmony_wallets.csv")




