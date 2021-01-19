## Install pymongo and dnspython via pip3 (terminal in Pycharm/Jupyter Notebook)
# pip3 install pymongo
# pip3 install dnspython

from main import Block
import pymongo
import datetime
import json
import pandas as pd
import itertools

# initializes variables
hash_list = []
chain = []
difficulty_list = []
block = Block(0, "", 1, "", "", 2, 0)
index = 0
json_dict = {}
corrupt_block_hash = ""

# importing the connection string from a text file
filepath = "C:/Users/sameer.sakkhari/Desktop/"
txtfile = input("What is the connect file titled (do not enter extension)\n")
ext = ".txt"
try:
    with open(filepath + txtfile + ext) as data_file:
        connection_string = json.load(data_file)
        client = pymongo.MongoClient(connection_string['dbconnect'])
        names = client.list_database_names()
        db = client[connection_string['db']]
        collection = connection_string['collection']
except FileNotFoundError:
    print("File does not exist")


# reading the existing documents from mongo db
for document in db[collection].find({}, {"_id": 0}):
    chain.append(document)
    data = document["data"]
    previousHash = document["previousHash"]
    nonce = document["nonce"]
    sender = document["sender"]
    recipient = document["recipient"]
    difficulty = document["difficulty"]
    index = document["index"]
    block = Block(data, previousHash, nonce, sender, recipient, difficulty, index)
    chain_hash = block.recompute_hash(data, previousHash, nonce, sender, recipient, difficulty)
    hash_list.append(chain_hash)
    difficulty_list.append(difficulty)
    index += 1

# if there are no documents in mongodb, then adding genesis block
if not chain:
    chain.append(block.create_genesisBlock())
    chain_hash = block.recompute_hash(0, "", 1, "", "", 2)
    hash_list.append(chain_hash)
    difficulty_list.append(2)
    post = {"data": 0, "previousHash": "", "nonce": block.nonce, "sender": "", "recipient": "", "difficulty": 2,
            "index": 0}
    db[collection].insert_one(post)
    index += 1

# options for performing actions on blockchain stored in mongodb
print("1. Adding transaction to blockchain")
print("2. Verify the blockchain")
print("3. View the blockchain")
print("4. Corrupt a block")
print("5. Fix corruption by recomputing hashes")
print("6. Export the blockchain to txt in json format")
print("7. Compare blockchain against the one stored in txt file")
print("8. Query")
print("9. Terminate program")
print("-----------------------------------------------------------------")

# while loop which performs several actions based on what option is chosen by the user
while True:
    selection = input("Enter Selection: ")

    # adds transactions to the existing blockchain
    if selection == '1':
        data = int(input("Enter data field: "))
        sender = input("Enter sender's name: ")
        recipient = input("Enter recipient's name: ")
        difficulty = int(input("Enter difficulty level: "))
        print("-------------------------------------------------------")
        previousHash = chain_hash
        nonce = 1
        block = Block(data, previousHash, nonce, sender, recipient, difficulty, index)
        chain_hash = block.recompute_hash(data, previousHash, nonce, sender, recipient, difficulty)
        chain.append(block.__dict__)
        hash_list.append(chain_hash)
        difficulty_list.append(difficulty)
        post = {"data": data, "previousHash": previousHash, "nonce": block.nonce, "sender": sender,
                "recipient": recipient, "difficulty": difficulty, "index": index}
        db[collection].insert_one(post)
        index += 1

    elif selection == '2':
        # when reading the existing documents from mongodb, it checks for verification
        if len(corrupt_block_hash) == 0:
            index = 1
            for document in db[collection].find({}, {"_id": 0}).skip(1):
                if document["previousHash"] == hash_list[index - 1]:
                    print("Blockchain is verified. No corruption at block " + str(index - 1))
                    index += 1
                else:
                    print(document["previousHash"])
                    print(hash_list)
                    print("Corruption occurred at block: " + str(index - 1))
                    index += 1
                    break
                #print("Blockchain is verified. No corruption ")

        # if a block is corrupted
        else:
            print("Corruption occurred at block: " + str(index))

    # views the blockchain
    elif selection == '3':
        for document in db[collection].find({}, {"_id": 0}):
            print(document)
            print("-------------------------------------------------------")

    # corrupts a blockchain based on the index input by the user.
    elif selection == '4':
        print("Enter a block index [0-1]\n")
        index = int(input("Enter block index\n"))
        new_data = input("Enter new data field, if empty string data will be unchanged\n")
        data = int(new_data) if not len(new_data) == 0 else chain[index]['data']

        new_sender = input("Enter new sender field, if empty string sender will be unchanged\n")
        sender = new_sender if not len(new_sender) == 0 else chain[index]['sender']

        new_recipient = input("Enter new recipient field, if empty string recipient will be unchanged\n")
        recipient = new_recipient if not len(new_recipient) == 0 else chain[index]['recipient']
        print("-----------------------------------------------------------------------------")

        if index == 0:
            previousHash = chain[index]['previousHash']
            difficulty = chain[index]['difficulty']
            nonce = chain[index]['nonce']
            block = Block(data, previousHash, nonce, sender, recipient, difficulty, index)
            corrupt_block_hash = block.recompute_hash(data, previousHash, nonce, sender, recipient, difficulty)
            chain[index] = block.__dict__
            db[collection].replace_one({"index": index},
                                       {"data": data, "previousHash": previousHash, "nonce": nonce,
                                        "sender": sender,
                                        "recipient": recipient, "difficulty": difficulty, "index": index})

        # if the user wants to corrupt a block other than genesis block
        else:
            previousHash = chain[index]['previousHash']
            difficulty = chain[index]['difficulty']
            nonce = chain[index]['nonce']
            block = Block(data, previousHash, nonce, sender, recipient, difficulty, index)
            corrupt_block_hash = block.recompute_hash(data, previousHash, nonce, sender, recipient, difficulty)
            chain[index] = block.__dict__
            db[collection].replace_one({"index": index},
                                       {"data": data, "previousHash": previousHash, "nonce": nonce,
                                        "sender": sender,
                                        "recipient": recipient, "difficulty": difficulty, "index": index})

    # recomputes hashes for the blockchain after a block is corrupted
    elif selection == '5':
        for i in range(index, len(chain)):
            data = chain[i]['data']
            sender = chain[i]['sender']
            recipient = chain[i]['recipient']
            difficulty = chain[i]['difficulty']
            previousHash = chain[i]['previousHash'] if i == index else chain_hash
            nonce = chain[i]['nonce']
            index = chain[i]['index']
            block = Block(data, previousHash, nonce, sender, recipient, difficulty, index)
            chain_hash = block.recompute_hash(data, previousHash, nonce, sender, recipient, difficulty)
            hash_list[i] = chain_hash
            chain[i] = block.__dict__
            db[collection].replace_one({"index": index},
                                       {"data": data, "previousHash": previousHash, "nonce": block.nonce,
                                        "sender": sender,
                                        "recipient": recipient, "difficulty": difficulty, "index": index})
        corrupt_block_hash = ""
        print("Some corruption was found. Fixed corruption by recomputing hashes")
        print("----------------------------------------------------------------------------")

    # saves the blockchain in the json format
    elif selection == '6':
        filepath = "C:/Users/sameer.sakkhari/Desktop/"
        txtfile = input("What is the filename you want to save the blockchain to? (do not include extension)\n")
        ext = ".txt"
        json_dict["chainHash"] = hash_list[-1]
        json_dict["difficulty"] = difficulty_list
        json_dict["Blockchain"] = chain
        json_obj = json.dumps(json_dict)
        with open(filepath + txtfile + ext, "w") as f:
            f.write(json_obj)
        print("File saved as: " + txtfile + ext)
        print("-------------------------------------------------------------------------------")

    # compares the blockchain stored in the mongo db against blockchain saved in json format in a text file
    elif selection == '7':
        filename = input('Enter filename you want to compare blockchain against\n ')
        extension = ".txt"
        filepath = "C:/Users/sameer.sakkhari/Desktop/"
        with open(filepath + filename + extension) as data_file:
            data = json.load(data_file)
            if data['Blockchain'] == chain:
                print('identical blockchain')
            else:
                for i in range(min(len(data['Blockchain']), len(chain))):
                    if data['Blockchain'][i] != chain[i]:
                        print("non identical blockchain at block " + str(i))
                        break
        print("-------------------------------------------------------------------------------")

    # queries for fetching blocks based data, sender and recipient field specified by the user
    elif selection == '8':
        print("Case 1: If you want to search by sender, recipient and transaction amt.")
        print("Case 2: If you want to search by sender and transaction amt.")
        print("Case 3: If you want to search by recipient and transaction amt.")
        print("Case 4: If you want to search by sender and recipient.")
        print("Case 5: If you want to search by sender only.")
        print("Case 6: If you want to search by recipient only.")
        print("Case 7: If you want to search by transaction amt only.")
        print("Case 8: Exit.")
        print("-----------------------------------------------------------------")

        while True:
            case = input("Which case do you want to select: ")
            mycol = db[collection]
            if case == '1':
                sender = input(
                    "Would you like to search for a sender?, enter anything other than empty string for yes\n")
                recipient = input(
                    "Would you like to search for a recipient?, enter anything other than empty string for yes\n")
                trxn_amt_gt = input(
                    "Do you want to search for transactions > an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_gt) == 0:
                    trxn_amt_gt = int(trxn_amt_gt)
                    mydoc = mycol.find({"sender": sender, "recipient": recipient, "data": {"$gt": trxn_amt_gt}},
                                       {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue
                trxn_amt_lt = input(
                    "Do you want to search for transactions < an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_lt) == 0:
                    trxn_amt_lt = int(trxn_amt_lt)
                    mydoc = mycol.find({"sender": sender, "recipient": recipient, "data": {"$lt": trxn_amt_lt}},
                                       {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue
                trxn_amt = input(
                    "Do you want to search for transactions = an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt) == 0:
                    trxn_amt = int(trxn_amt)
                    mydoc = mycol.find({"sender": sender, "recipient": recipient, "data": trxn_amt}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

            elif case == '2':
                sender = input(
                    "Would you like to search for a sender?, enter anything other than empty string for yes\n")
                trxn_amt_gt = input(
                    "Do you want to search for transactions > an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_gt) == 0:
                    trxn_amt_gt = int(trxn_amt_gt)
                    mydoc = mycol.find({"sender": sender, "data": {"$gt": trxn_amt_gt}}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue
                trxn_amt_lt = input(
                    "Do you want to search for transactions < an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_lt) == 0:
                    trxn_amt_lt = int(trxn_amt_lt)
                    mydoc = mycol.find({"sender": sender, "data": {"$lt": trxn_amt_lt}}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue
                trxn_amt = input(
                    "Do you want to search for transactions = an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt) == 0:
                    trxn_amt = int(trxn_amt)
                    mydoc = mycol.find({"sender": sender, "data": trxn_amt}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

            elif case == '3':
                recipient = input(
                    "Would you like to search for a recipient?, enter anything other than empty string for yes\n")
                trxn_amt_gt = input(
                    "Do you want to search for transactions > an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_gt) == 0:
                    trxn_amt_gt = int(trxn_amt_gt)
                    mydoc = mycol.find({"recipient": recipient, "data": {"$gt": trxn_amt_gt}}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

                trxn_amt_lt = input(
                    "Do you want to search for transactions < an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_lt) == 0:
                    trxn_amt_lt = int(trxn_amt_lt)
                    mydoc = mycol.find({"recipient": recipient, "data": {"$lt": trxn_amt_lt}}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

                trxn_amt = input(
                    "Do you want to search for transactions = an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt) == 0:
                    trxn_amt = int(trxn_amt)
                    mydoc = mycol.find({"recipient": recipient, "data": trxn_amt}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

            elif case == '4':
                sender = input(
                    "Would you like to search for a sender?, enter anything other than empty string for yes\n")
                recipient = input(
                    "Would you like to search for a recipient?, enter anything other than empty string for yes\n")
                mydoc = mycol.find({"sender": sender, "recipient": recipient}, {"_id": 0})
                for x in mydoc:
                    print(x)
                continue

            elif case == '5':
                sender = input(
                    "Would you like to search for a sender?, enter anything other than empty string for yes\n")
                mydoc = mycol.find({"sender": sender}, {"_id": 0})
                for x in mydoc:
                    print(x)
                continue

            elif case == '6':
                recipient = input(
                    "Would you like to search for a recipient?, enter anything other than empty string for yes\n")
                mydoc = mycol.find({"recipient": recipient}, {"_id": 0})
                for x in mydoc:
                    print(x)
                continue

            elif case == '7':
                trxn_amt_gt = input(
                    "Do you want to search for transactions > an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_gt) == 0:
                    trxn_amt_gt = int(trxn_amt_gt)
                    mydoc = mycol.find({"data": {"$gt": trxn_amt_gt}}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

                trxn_amt_lt = input(
                    "Do you want to search for transactions < an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt_lt) == 0:
                    trxn_amt_lt = int(trxn_amt_lt)
                    mydoc = mycol.find({"data": {"$lt": trxn_amt_lt}},
                                       {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

                trxn_amt = input(
                    "Do you want to search for transactions = an amount? Enter amount if you do otherwise empty string ")
                if not len(trxn_amt) == 0:
                    trxn_amt = int(trxn_amt)
                    mydoc = mycol.find({"data": trxn_amt}, {"_id": 0})
                    for x in mydoc:
                        print(x)
                    continue

            elif case == '8':
                break

    elif selection == '9':
        break
