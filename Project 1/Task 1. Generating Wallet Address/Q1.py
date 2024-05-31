import os
import bech32
import base58
import base64
import ecdsa
import hashlib


def address_generation():
    private_key = os.urandom(32).hex()
    sk = ecdsa.SigningKey.from_string(
        bytes.fromhex(private_key), ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = (b'\x04' + vk.to_string()).hex()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(bytes.fromhex(public_key)).digest())
    middle = b'\x6f' + ripemd160.digest()
    checksum = hashlib.sha256(hashlib.sha256(middle).digest()).digest()[:4]
    binary_addr = middle + checksum
    addr = base58.b58encode(binary_addr)
    return private_key, public_key, addr


def wif_formatter(private_key):
    wif_private_key = b'\x80' + bytes.fromhex(private_key) + b'\x01'
    checksum2 = hashlib.sha256(hashlib.sha256(
        wif_private_key).digest()).digest()[:4]
    wif_private_key = wif_private_key + checksum2
    return wif_private_key


prv_key, pub_key, addr = address_generation()
print("BTC address: " + addr.decode("utf-8"))


wif_prv_key = wif_formatter(prv_key)
print("wif private key in base 58 : " +
      base58.b58encode(wif_prv_key).decode("utf-8"))
