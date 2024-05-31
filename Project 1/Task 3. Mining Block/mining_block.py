from hashlib import sha256
MAX_NONCE = 100000000000
n = 9259

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()


def mine(block_number, transactions, previous_hash, prefix_zeros):
    prefix_str = '0'*prefix_zeros
    for nonce in range(MAX_NONCE):
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            print(f"Successfully mined bitcoins with nonce value:{nonce}")
            return new_hash

    raise BaseException(
        f"Couldn't find correct has after trying {MAX_NONCE} times")


if __name__ == '__main__':
    coinbase = {"reward": 6.25,
                "data": "383130313939323539416c6972657a614d6f6873656e69",
                "destination": "mpNvmLAb9hYJ1q2BFcCbnsfKNNLGxVtW8o"
                }

    block = {
        "header": {
            "coinbase": coinbase,
            "merkle_root": SHA256(str(coinbase))
        },
        "transactions": []
    }
    difficulty = 4
    previous_hash = "010000000c264b615aa71991ce55d04035470887eec8d56b2272909ed04649c0000000001a54f5af8ab756ff6ec14308e8a251649c7fb60ff84f0704ebe016b507a839770a1dd149ffff001d2655c8a90101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0804ffff001d020d01ffffffff0100f2052a01000000434104e95ed1a7013b48ca943f2d33b7b36030b346e0e7b25e9c49332eebb73b2d7a333f43eaa635d98a2c895f2b017470bb83e71dab694bbfcbcefd66e69ed4adb3e8ac00000000"
    block_number = 9257
    new_hash = mine(block_number, str(block), previous_hash, difficulty)
    print(new_hash)
    print(block)