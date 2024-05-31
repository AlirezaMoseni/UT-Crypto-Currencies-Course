import bitcoin.wallet ,hashlib
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
from Crypto.Hash import RIPEMD160

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("cS3Ykn28yDPagMXBgUNkrSdxzT3Hii5g2LgAQb2yN4kWJwWJ99Gg") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
# destination_address = bitcoin.wallet.CBitcoinAddress('') # Destination address (recipient of the money)
# destination_address2 = bitcoin.wallet.CBitcoinAddress('') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(address):

    return [ OP_DUP , OP_HASH160 ,address , OP_EQUALVERIFY  ,OP_CHECKSIG]

def P2PKH_scriptPubKey_NOBODY():

    return [OP_RETURN]

def P2PKH_scriptPubKey_EVERYBODY():

    return []

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):

    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature , my_public_key]


def send_from_P2PKH_transaction(amount_to_send,amount_to_send2, txid_to_spend, utxo_index,
                                txout_scriptPubKey,txout_scriptPubKey2 ):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txout2 = create_txout(amount_to_send2, txout_scriptPubKey2)
    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, [txout,txout2] , txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, [txout,txout2], txin_scriptPubKey,
                                       txin_scriptSig)
    return broadcast_transaction(new_tx)

def create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [txout[0],txout[1]])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig


def create_signed_transaction(txin, txout, txin_scriptPubKey,txin_scriptSig):
    tx = CMutableTransaction([txin], [txout[0],txout[1]])
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.00002
    amount_to_send2 = 0.00007
    txid_to_spend = ('3d628c35a628f963b61c0c323da805ffacf2d8d5769f06cf47983abb637f37aa')    # TxHash of UTXO
    utxo_index = 1     # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey_NOBODY()
    txout_scriptPubKey2 = P2PKH_scriptPubKey_EVERYBODY()
    response = send_from_P2PKH_transaction(amount_to_send,amount_to_send2, txid_to_spend, utxo_index,
                                           txout_scriptPubKey,txout_scriptPubKey2)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

