import hashlib
import time
import random
import string

class Block:
    def __init__(self, version, previous_hash, merkle_root, timestamp, bits, nonce, transactions=None):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.transactions = transactions if transactions else []

    def hash_block(self):
        block_header = (str(self.version) +
                        str(self.previous_hash) +
                        str(self.merkle_root) +
                        str(self.timestamp) +
                        str(self.bits) +
                        str(self.nonce))
        return hashlib.sha256(block_header.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(version=1,
                              previous_hash="0" * 32,
                              merkle_root="0" * 32,
                              timestamp=int(time.time()),
                              bits=0,
                              nonce=0
                              )
        genesis_block.hash = genesis_block.hash_block()
        self.chain.append(genesis_block)

    def add_block(self, version, bits, transactions):
        previous_block = self.chain[-1]
        merkle_tree = MerkleTree(transactions)
        new_block = Block(version=version,
                          previous_hash=previous_block.hash,
                          merkle_root=merkle_tree.root(),
                          timestamp=int(time.time()),
                          bits=bits,
                          nonce=0,
                          transactions=transactions
                          )
        new_block.nonce = self.proof_of_work(new_block)
        new_block.hash = new_block.hash_block()
        self.chain.append(new_block)

    def proof_of_work(self, block, difficulty=4): 
        target = "0" * difficulty
        nonce = 0
        while True:
            block.nonce = nonce
            hash_val = block.hash_block()
            if hash_val.startswith(target):
                return nonce
            nonce += 1

class MerkleTree:
    def __init__(self, data):
        self.data = data
        self.tree = self.build_tree()

    def build_tree(self):
        # Ensure the number of transactions is a power of 2
        while len(self.data) & (len(self.data) - 1) != 0 or len(self.data) == 1:
            self.data.append("")  # Padding with empty strings
        
        data_hashed = [self.hash(d) for d in self.data]
        tree = [data_hashed]

        while len(data_hashed) > 1:
            data_hashed = [self.hash(data_hashed[i] + data_hashed[i + 1]) for i in range(0, len(data_hashed), 2)]
            tree.insert(0, data_hashed)

        return tree

    def hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def root(self):
        return self.tree[0][0]

if __name__ == "__main__":
    transaction = ['Transaction1', 'Transaction2', 'Transaction3', 'Transaction4']
    blockchain = Blockchain()
    
    blockchain.add_block(version=2, bits=1234, transactions=transaction)
    
    for i in range(2, 6):
        random_transactions = [f'Transaction{i}{j}' for j in range(1, random.randint(2, 5))]  # Tạo ngẫu nhiên từ 2 đến 4 giao dịch cho mỗi block
        blockchain.add_block(version=random.randint(1, 100), bits=random.randint(1000, 9999), transactions=random_transactions)


    print("Blockchain length:", len(blockchain.chain))
    for i, block in enumerate(blockchain.chain):
        print(f"Block {i}: {block.hash_block()}")
        print("Transactions:", block.transactions)
        print("Merkle Root:", block.merkle_root)
        print("")
        
        