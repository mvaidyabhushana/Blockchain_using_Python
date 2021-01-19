import hashlib
import json


# creating a Block with all the transactions which user enters
# Each transactions consists of data, sender, recipient and difficulty : user entered
# nonce, previous hash, nonce and index : program calculated
class Block:

    def __init__(self, data, previousHash, nonce, sender, recipient, difficulty, index):
        self.data = int(data)
        self.previousHash = str(previousHash)
        self.nonce = int(nonce)
        self.sender = str(sender)
        self.recipient = str(recipient)
        self.difficulty = int(difficulty)
        self.index = int(index)

    def create_genesisBlock(self):
        first_block = {"data": 0, "previousHash": "", "nonce": 563, "sender": "", "recipient": "",
                       "difficulty": 2, "index": 0}
        return first_block

        # for every block, it computes hash value

    def compute_hash(self, data, previousHash, nonce, sender, recipient):
        block_string = str(data) + str(previousHash) + str(nonce) + str(sender) + str(recipient)
        return hashlib.sha256(block_string.encode()).hexdigest()

    # recalculates hash value based on the difficulty entered for the particular block
    def recompute_hash(self, data, previousHash, nonce, sender, recipient, difficulty):
        validity = False
        recomputed_hash = self.compute_hash(data, previousHash, nonce, sender, recipient)

        while not validity:
            if recomputed_hash.startswith('0' * int(difficulty)):
                return recomputed_hash
            nonce += 1
            recomputed_hash = self.compute_hash(data, previousHash, nonce, sender, recipient)
            self.nonce = nonce
        return recomputed_hash



