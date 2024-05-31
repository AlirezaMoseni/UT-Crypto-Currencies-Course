import bitcoin.wallet ,hashlib
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
from Crypto.Hash import RIPEMD160

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("cS3Ykn28yDPagMXBgUNkrSdxzT3Hii5g2LgAQb2yN4kWJwWJ99Gg") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address1 = bitcoin.wallet.CBitcoinAddress('mrrJH8rfQswojwztr2pGNsdbdz6hELXg85') # Destination address (recipient of the money)
destination_address2 = bitcoin.wallet.CBitcoinAddress('mxg8CPu3UT1ZvfiaRBW12HKouoCW1oqAvp') # Destination address (recipient of the money)
destination_address3 = bitcoin.wallet.CBitcoinAddress('msgjfBCqVwSvTvzBiLpYQGD1MHXbfY5Ds5') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(address):

    return [ OP_DUP , OP_HASH160 ,address , OP_EQUALVERIFY  ,OP_CHECKSIG]

def P2MS_scriptPubKey(pkey1, pkey2, pkey3):

    return [OP_2, pkey1, pkey2, pkey3, OP_3 , OP_CHECKMULTISIG]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):

    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature , my_public_key]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey ):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout ,txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.0009
    txid_to_spend = ('3b27769a29955c47fcc209445316dd38c40b9ac3d6cc214186465b7050a6fee1') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2MS_scriptPubKey(destination_address1, destination_address2, destination_address3)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                           txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result