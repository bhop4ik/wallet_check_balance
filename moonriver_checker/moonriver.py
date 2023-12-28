import asyncio
import aiohttp
import csv

# Define the RPC endpoint URL
CONFLUX_RPC_URL = 'https://moonriver.publicnode.com'

async def fetch(session, payload):
    async with session.post(CONFLUX_RPC_URL, json=payload) as response:
        return await response.json()

async def get_balance(session, address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    response = await fetch(session, payload)
    result = response.get('result', '0x0')
    balance = int(result, 16) / 10**18  # Assuming CFX has 18 decimal places
    return balance

async def get_transaction_count(session, address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [address, "latest"],
        "id": 1
    }
    response = await fetch(session, payload)
    result = response.get('result', '0x0')
    transaction_count = int(result, 16)
    return transaction_count

async def main():
    # Read wallet addresses from 'wallets.txt'
    with open('wallets.txt', 'r') as file:
        wallet_addresses = [line.strip() for line in file if line.strip()]

    # Create a CSV file to store the data
    with open('wallet_moonriver.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Wallet', 'Native Token Amount (movr)', 'TX Count'])

        # Use aiohttp ClientSession for fetching data
        async with aiohttp.ClientSession() as session:
            # Prepare tasks for all wallets
            tasks = []
            for address in wallet_addresses:
                tasks.append(get_balance_and_tx_count(session, writer, address))
            
            # Await all tasks to complete
            await asyncio.gather(*tasks)

async def get_balance_and_tx_count(session, writer, address):
    balance = await get_balance(session, address)
    transaction_count = await get_transaction_count(session, address)
    writer.writerow([address, balance, transaction_count])

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
    print("Data has been written to wallet_moonriver.csv")