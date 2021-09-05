# Seasonal Tokens Miner

This is a python implementation of a miner for the Seasonal Tokens. 

## Installation

    $ pip3 install pysha3 web3
    $ git clone https://github.com/seasonaltokens/seasonaltokens-miner.git
    $ cd seasonaltokens-miner
    $ python3 seasonal_miner.py

    usage: python3 seasonal_miner.py <provider_url> <season> [reward batch size]

## Mining

To mine, you will need the URL of a provider that allows you to interact with the network. You can get one from [infura.io](https://infura.io). Create an account, start a new ethereum project, navigate to it, then go to Settings -> Keys -> Endpoints. Copy and save the URL that starts with "https://mainnet.infura.io/...".

You will also need the private key of an ethereum address that contains some ETH to pay for minting transactions. Export the private key from that account by clicking the three vertical dots at the top right of the MetaMask dialog and selecting Account Details -> Export Private Key.

Then you can mine, for example, Spring Tokens, by doing:

    $ python3 seasonal_miner.py <provider_url> spring

You can optionally add a final argument to specify the minimum number of rewards for which you are willing to pay the ETH costs of submitting the transaction that claims the tokens:

    $ python3 seasonal_miner.py <provider_url> spring 5

The default value is 1.

The mining software will then prompt you for the private key and begin mining. The user will be prompted for confirmation if there are more rewards currently available than the specified minimum.

## Adding the Tokens to MetaMask

To see and send the tokens mined, you need to add the tokens to your account in MetaMask. In the MetaMask dialog, select your account and click the Add Token button at the bottom of your list of Assets. Then paste the contract address of the token you want to add:

    spring: 0xf04aF3f4E4929F7CD25A751E6149A3318373d4FE
    summer: 0x4D4f3715050571A447FfFa2Cd4Cf091C7014CA5c
    autumn: 0x4c3bAe16c79c30eEB1004Fb03C878d89695e3a99
    winter: 0xCcbA0b2bc4BAbe4cbFb6bD2f1Edc2A9e86b7845f

