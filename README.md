# Seasonal Tokens Miner

This is a python implementation of a miner for the Seasonal Tokens. At present, it mines on the Rinkeby test network.

## Installation

    $ pip3 install pysha3 web3
    $ python3 seasonal_miner_rinkeby.py

    usage: python seasonal_miner.py <provider_url> <private key> <season> [reward batch size]

## Mining

To mine, you will need the URL of a provider that allows you to interact with the network. You can get one from [infura.io](https://infura.io). Create an account, start a new ethereum project, navigate to it, then go to Settings -> Keys -> Endpoints and select Rinkeby. Copy and save the URL that starts with "https://rinkeby.infura.io/...".

You will also need the private key of an ethereum address that contains some Rinkeby test ETH. Install the MetaMask plugin in your browser and connect it to RInkeby by clicking on Ethereum Mainnet at the top of the MetaMask dialog box and selecting Rinkeby Test Network from the drop-down menu.

Then go to https://app.mycrypto.com/ and connect the website to MetaMask by clicking on the MetaMask icon. Then go to Tools -> Use TestNet Faucet, select your MetaMask account, click Request Assets and complete the captcha. It should send a small amount of test ETH to you, which should be visible in MetaMask after about 30 seconds.

Then export the private key from that account by clicking the three vertical dots at the top right of the MetaMask dialog and selecting Account Details -> Export Private Key.

Then you can mine, for example, Spring Tokens, by doing:

    $ python3 seasonal_miner_rinkeby.py <provider_url> <private key> spring

You can optionally add a final argument to specify the minimum number of rewards for which you are willing to pay the ETH costs of submitting the transaction that claims the tokens:

    $ python3 seasonal_miner_rinkeby.py <provider_url> <private key> spring 5

The default value is 1.

## Adding the Tokens to MetaMask

To see and send the tokens mined, you need to add the tokens to your account in MetaMask. In the MetaMask dialog, select your account and click the Add Token button at the bottom of your list of Assets. Then paste the contract address of the token you want to add:

    spring: 0xc46C470A632f4A20396DCF15fE760D536BB0eE62
    summer: 0x30db052576fb86E505F7257a42Fb25493503dFcc
    autumn: 0x448d91A2447cB8153C8aaB389Bea51c46B81f8df
    winter: 0x51df120A37a2401e37c7FEB33Fc47b09B6617579


