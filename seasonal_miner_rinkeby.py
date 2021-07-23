import sys
import json
from web3 import Web3
import codecs
from random import getrandbits
import sha3
from web3.middleware import construct_sign_and_send_raw_middleware, geth_poa_middleware
from time import time, sleep


seasons = ["spring", "summer", "autumn", "winter"]

contract_addresses = {'spring': '0xc46C470A632f4A20396DCF15fE760D536BB0eE62',
                      'summer': '0x30db052576fb86E505F7257a42Fb25493503dFcc',
                      'autumn': '0x448d91A2447cB8153C8aaB389Bea51c46B81f8df',
                      'winter': '0x51df120A37a2401e37c7FEB33Fc47b09B6617579'}

ABI = json.load(open("SeasonalToken.ABI"))


class SeasonalTokenMiner(object):
    def __init__(self, provider_url, private_key, season, batch_size):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        # middleware for Rinkeby test network
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contracts = dict([(season, 
                                self.w3.eth.contract(address=contract_addresses[season], 
                                                     abi=ABI))
                               for season in seasons])
        self.season = season
        self.contract = self.contracts[season]
        self.batch_size = batch_size
        self.private_key = private_key
        self.account = self.w3.eth.account.privateKeyToAccount(private_key)
        self.address = codecs.decode(self.account.address.replace("0x", ""),'hex_codec')
        self.start = time()
        self.hashes = 0

    def get_challenge_and_mining_target(self):
        return self.contract.caller.getChallengeNumber(), self.contract.caller.getMiningTarget()

    def generate_nonce(self):
        myhex =  b'%064x' % getrandbits(32*8)
        return codecs.decode(myhex, 'hex_codec')

    def get_mean_expected_reward_time(self, hashrate, mining_target):
        return mining_target / hashrate

    def get_mean_expected_reward_time_in_minutes(self, hashrate, mining_target):
        return self.get_mean_expected_reward_time(hashrate, 2**256/mining_target) / 60

    def print_hashrate(self, mining_target):
        hashrate = self.hashes / (time() - self.start)
        reported_reward_rate = "%.2f" % self.get_mean_expected_reward_time_in_minutes(hashrate, mining_target)
        reported_hashrate = "%.2f" % hashrate
        sys.stdout.write("\rhashrate: " + reported_hashrate 
                         + "\t Expect rewards every "+ reported_reward_rate + " minutes")

    def mine(self, challenge, mining_target, timeout=10):
        self.start = time()
        self.hashes = 0
        while time() < self.start + timeout:
            nonce = self.generate_nonce()
            hash1 = int(sha3.keccak_256(challenge+self.address+nonce).hexdigest(), 16)
            if hash1 < mining_target:
                return nonce, hash1
            else:
                self.hashes += 1
                if self.hashes % 100000 == 0:
                    self.print_hashrate(mining_target)
        return None, None

    def mine_until_successful(self):        
        challenge, nonce, digest = (None, None, None)
        while (nonce, digest) == (None, None):
            challenge_, mining_target_ = self.get_challenge_and_mining_target()
            if challenge_ != challenge:
                print("\nsolving challenge", challenge_)
                challenge = challenge_
                print("")
            nonce, digest = self.mine(challenge_, mining_target_ // batch_size)
            if self.get_challenge_and_mining_target() != (challenge_, mining_target_):
                nonce, digest = (None, None)
        print("")
        print("Found solution")
        return challenge, nonce, digest

    def time_until_max_reward_available(self):
        if self.number_of_rewards_available() >= self.batch_size:
            return 0
        return (self.contract.caller.lastRewardBlockTime() + 600 * batch_size - time())

    def waited_for_max_reward_without_challenge_changing(self, challenge):
        while self.number_of_rewards_available() < self.batch_size:
            if self.get_challenge_and_mining_target()[0] != challenge:
                return False
            time_left = self.time_until_max_reward_available()
            print("Max rewards available:", self.number_of_rewards_available(),
                  "  Waiting for:", batch_size, "  estimated time left:", 
                   str(int(time_left // 60)).zfill(2)+":"+str(int(time_left % 60)).zfill(2))
            sleep(5)
        return True

    def send_mint_transaction(self, nonce, digest):
        self.w3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.account))
        self.w3.eth.default_account = self.account.address
        txn_hash = self.contract.functions.mint(nonce, digest).transact()
        return self.w3.eth.wait_for_transaction_receipt(txn_hash)

    def number_of_rewards_available(self):
        latest_block_time = self.w3.eth.get_block('latest').timestamp
        return self.contract.caller.getNumberOfRewardsAvailable(latest_block_time)

    def mine_and_send_mint_transaction(self):
        challenge, nonce, digest = self.mine_until_successful()
        while not self.waited_for_max_reward_without_challenge_changing(challenge):
            challenge, nonce, digest = self.mine_until_successful()
        nonce_int = int.from_bytes(nonce, "big")
        digest_hex = "{0:#0{1}x}".format(digest, 66)
        digest_bytes = bytearray.fromhex(digest_hex.replace("0x", ""))
        print("sending mint transaction")
        return self.send_mint_transaction(nonce_int, digest_bytes)

    def run(self):
        while True:
            print(self.mine_and_send_mint_transaction())


if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("usage: python seasonal_miner.py <provider_url> <private key> <season> [reward batch size]")
        sys.exit()
    provider_url, private_key, season = sys.argv[1:4]
    batch_size = int(sys.argv[4]) if len(sys.argv) == 5 else 1
    

    miner = SeasonalTokenMiner(provider_url, private_key, season, batch_size)

    if miner.number_of_rewards_available() > batch_size:
        print(miner.number_of_rewards_available(), 
              "rewards are available: Are you sure you can mine profitably with",
              batch_size, "rewards? (y/N): ",)
        if sys.stdin.readline().strip().lower() != "y":
            sys.exit()

    
    miner.run()
