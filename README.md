# Blockchain_using_Python

In this project I have created a blockchain from scratch using Python. Here are the following imports for my application: 
1. Json 
2. hashlib 
3. PyMongo
4. pandas

## What is Blockchain Technology?
Blockchain, also known as Distributed Ledger Technology (DLT), makes the history of any digital asset unalterable and transparent through the use of decentralization and cryptographic hashing. 

## How Does Blockchain Work?
Blockchain is a connected sequence of blocks.

### Blocks
Every chain consists of multiple blocks and each block has five basic elements:

- The data in the block.
- A 32-bit whole number called a nonce. The nonce is randomly generated when a block is created, which then generates a block header hash. 
- The hash is a 256-bit number wedded to the nonce. It must start with a huge number of zeroes (i.e., be extremely small)
- The sender's name who sends the transactions.
- The reciever's name who recieves the transactions.

When the first block of a chain is created, a nonce generates the cryptographic hash. The data in the block is considered signed and forever tied to the nonce and hash unless it is mined. 

### Miners
Miners create new blocks on the chain through a process called mining.

In a blockchain every block has its own unique nonce and hash, but also references the hash of the previous block in the chain, so mining a block isn't easy, especially on large chains.

Miners use special software to solve the incredibly complex math problem of finding a nonce that generates an accepted hash. Because the nonce is only 32 bits and the hash is 256, there are roughly four billion possible nonce-hash combinations that must be mined before the right one is found. When that happens miners are said to have found the "golden nonce" and their block is added to the chain. 

Making a change to any block earlier in the chain requires re-mining not just the block with the change, but all of the blocks that come after. This is why it's extremely difficult to manipulate blockchain technology. Think of it is as "safety in math" since finding golden nonces requires an enormous amount of time and computing power.

When a block is successfully mined, the change is accepted by all of the nodes on the network and the miner is rewarded financially.

## Architecture of the application
The architecture for this project will be a blockchain class, containing a main method to test out the functionality of the blockchain. 
Each blockchain will also have a list containing the difficulties of each block based on which nonce of a block is calculated and so is hash value.
For example, since the genesis block (first block) should have a default difficulty of 2, perhaps we have 4 total blocks with block 1 having a difficulty of 4, block 2 having a difficulty of 3 and block 3 having a difficulty of 2.  Our blockchain would need a list with those difficulties = [2,4,3,2] so you can validate if a hash is valid.  

Every block will contain the following information:
1. data (this will be a string)
2. previousHash (this will be a string)
3. nonce (this will be an integer)
4. sender (this will be a string)
5. recipient (this will be a string)

In order to calculate the hash value of each block, I have concatenated the above parameters in the given order: (data+previousHash+nonce+sender+recipient) using SHA256.

All the blocks are stored as JSON objects.

