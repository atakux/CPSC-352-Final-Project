from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# public key used for encrypting, private key used for decrypting
def gen_public_private_keys() -> (RSA.RsaKey, RSA.RsaKey):
    # Generate a public and private key pair
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()

    return public_key, private_key

def export_private_key(private_key: RSA.RsaKey, filename) -> None:
    with open(filename, "wb") as file:
        file.write(private_key.export_key(format="PEM"))

def export_public_key(public_key: RSA.RsaKey, filename) -> None:
    with open(filename, "wb") as file:
        file.write(public_key.export_key(format="PEM"))

def import_private_key(filename) -> RSA.RsaKey:
    with open(filename, "rb") as file:
        private_key = RSA.import_key(file.read())
    
    return private_key

def import_public_key(filename) -> RSA.RsaKey:
    with open(filename, "rb") as file:
        public_key = RSA.import_key(file.read())
    
    return public_key

