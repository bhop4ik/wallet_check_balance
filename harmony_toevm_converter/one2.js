

const { Harmony } = require('@harmony-js/core');
const { ChainID, ChainType } = require('@harmony-js/utils');
const fs = require('fs');
const { createObjectCsvWriter } = require('csv-writer');

// Initialize Harmony instance
const hmy = new Harmony(
  'https://api.harmony.one',
  {
    chainType: ChainType.Harmony,
    chainId: ChainID.HmyMainnet,
  },
);

// Function to convert an ETH address to Harmony ONE address
const convertAddress = (ethAddress) => {
  return hmy.crypto.getAddress(ethAddress).bech32;
};

// Your text file with EVM addresses
const inputFile = 'evm_addresses.txt'; // Update with your input text file path
const outputFile = 'ONE_addresses.csv'; // The output CSV file path

// Read the input EVM (Ethereum) addresses from the txt file
const ethAddresses = fs.readFileSync(inputFile, 'utf8').trim().split('\n');

// Initialize CSV writer
const csvWriter = createObjectCsvWriter({
    path: outputFile,
    header: [
        {id: 'evmAddress', title: 'EVM_Address'},
        {id: 'oneAddress', title: 'ONE_Address'},
    ],
});

// Create an array to store the converted address objects
const addressMap = ethAddresses.map((address) => ({
  evmAddress: address,
  oneAddress: convertAddress(address),
}));

// Write to the CSV file
csvWriter.writeRecords(addressMap)
  .then(() => {
    console.log(`Conversion complete. Harmony ONE addresses have been saved to ${outputFile}`);
  })
  .catch((err) => {
    console.error('An error occurred while writing the CSV file:', err);
  });


