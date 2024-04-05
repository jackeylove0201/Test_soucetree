from ecdsa import SigningKey, SECP256k1
import base58
import hashlib

def generate_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    
    public_key = private_key.get_verifying_key()
    
    return private_key, public_key

def pubkey_to_address(pubkey):

    sha256_pubkey = hashlib.sha256(pubkey).digest()

    ripemd160_pubkey = hashlib.new('ripemd160', sha256_pubkey).digest()

    extended_ripemd160_pubkey = b'\x00' + ripemd160_pubkey

    checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160_pubkey).digest()).digest()[:4]

    binary_address = extended_ripemd160_pubkey + checksum

    address = base58.b58encode(binary_address)

    return address.decode('utf-8')

def main():
    private_key, public_key = generate_keys()


    wallet_address = pubkey_to_address(public_key.to_string())
    print("Wallet Address: " + wallet_address)

if __name__ == "__main__":
    main()