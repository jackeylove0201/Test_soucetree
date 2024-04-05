from ecdsa import SigningKey, SECP256k1
import base58
import hashlib

def generate_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.verifying_key
    return private_key, public_key

def pubkey_to_address(pubkey):
    pubkey_bytes = pubkey.to_string()

    sha256_pubkey = hashlib.sha256(pubkey_bytes).digest()
    ripemd160_pubkey = hashlib.new('ripemd160', sha256_pubkey).digest()

    extended_ripemd160_pubkey = b'\x00' + ripemd160_pubkey

    checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160_pubkey).digest()).digest()[:4]
    binary_address = extended_ripemd160_pubkey + checksum

    address = base58.b58encode(binary_address)
    return address.decode('utf-8')


def privkey_to_address(privkey):
    # Tạo public key từ private key
    public_key = privkey.verifying_key.to_string()
    sha256_pubkey = hashlib.sha256(public_key).digest()
    ripemd160_pubkey = hashlib.new('ripemd160', sha256_pubkey).digest()
    extended_ripemd160_pubkey = b'\x00' + ripemd160_pubkey
    checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160_pubkey).digest()).digest()[:4]
    
    binary_address = extended_ripemd160_pubkey + checksum
    
    address = base58.b58encode(binary_address)
    return address.decode('utf-8')

def is_valid_btc_address(address):
    try:
        address_bytes = base58.b58decode(address)
        extended_ripemd160_pubkey = address_bytes[:-4]
        checksum = address_bytes[-4:]
        expected_checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160_pubkey).digest()).digest()[:4]
        return checksum == expected_checksum
    except:
        return False

def main():
    private_key, public_key = generate_keys()
    private_key_hex = private_key.to_string().hex()
    public_key_hex = public_key.to_string().hex()
    
    print("Private Key:", private_key_hex)
    print("Public Key:", public_key_hex)

    wallet_address = pubkey_to_address(public_key)
    print("Wallet Address:", wallet_address)
    print("kiểm tra Khoá:", is_valid_btc_address(wallet_address))

    file_path = "C:\\Users\\ADMIN\\Desktop\\wallet.txt"
    with open(file_path, 'w') as file:
        file.write(f"Private Key: {private_key_hex}\n")
        file.write(f"Public Key: {public_key_hex}\n")
        file.write(f"Wallet Address: {wallet_address}\n")
    print("Keys saved to:", file_path)

if __name__ == "__main__":
    main()
