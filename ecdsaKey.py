from ecdsa import SigningKey, VerifyingKey, NIST256p
import hashlib

def generate_keys():

    private_key = SigningKey.generate(curve=NIST256p)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def sign_message(private_key, message):
 
    signature = private_key.sign(message, hashfunc=hashlib.sha256)
    return signature

def verify_signature(public_key, signature, message):

    verified = public_key.verify(signature, message, hashfunc=hashlib.sha256)
    return verified

def save_keys_to_file(private_key, public_key, file_path):
    with open(file_path, 'w') as file:
        file.write("Private Key:")
        file.write(private_key.to_string().hex() + "\n")
        file.write("Public Key:")
        file.write(public_key.to_string().hex() + "\n")

def main():
    try:
        private_key, public_key = generate_keys()
        print("Private Key:", private_key.to_string().hex())
        print("Public Key:", public_key.to_string().hex())
    
        file_path = "C:\\VsCode\\Python_Blockchain\\input2.txt"
        save_keys_to_file(private_key, public_key, file_path)
        print("Keys saved to:", file_path)
      
        message = input("Enter your signature: ").encode()
        signature = sign_message(private_key, message)
        print("Signature:", signature.hex())


        verified = verify_signature(public_key, signature, message)
        print("Verified:", verified)


    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
