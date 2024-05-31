import bitcoin.wallet
import hashlib
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
from Crypto.Hash import RIPEMD160

bitcoin.SelectParams("testnet")
# Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_private_key = bitcoin.wallet.CBitcoinSecret(
    "cS3Ykn28yDPagMXBgUNkrSdxzT3Hii5g2LgAQb2yN4kWJwWJ99Gg")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress(
    'mpNvmLAb9hYJ1q2BFcCbnsfKNNLGxVtW8o')  # Destination address (recipient of the money)


def P2PKH_scriptPubKey(address):

    return [OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG]


def P2PKH_scriptPubKey_EVERYBODY(address):

    return []


def P2PKH_scriptSig_EVERYBODY():
    return [OP_TRUE]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):

    signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, my_private_key)

    return []


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey_EVERYBODY(my_address)
    txin = create_txin(txid_to_spend, utxo_index)

    txin_scriptSig = P2PKH_scriptSig_EVERYBODY()

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.00006
    # TxHash of UTXO
    txid_to_spend = ('a34d95fba359ef6a5359579157947e27450187004d742b4b67214df93d10d1a6')
    utxo_index = 1  # UTXO index among transaction outputs
    ######################################################################

    print(my_address)  # Prints your address in base58
    print(my_public_key.hex())  # Print your public key in hex
    print(my_private_key.hex())  # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(destination_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                           txout_scriptPubKey)
    print(response.status_code, response.reason)
    # Report the hash of transaction which is printed in this section result
    print(response.text)
