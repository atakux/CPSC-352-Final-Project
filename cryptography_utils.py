from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# public key used for encrypting, private key used for decrypting
def gen_public_private_keys() -> (RSA.RsaKey, RSA.RsaKey):
    """Generate a pub, priv key pair"""
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()

    return public_key, private_key

def export_key(key: RSA.RsaKey, filename) -> None:
    """Export either private or public key to a directory"""
    with open(filename, "wb") as file:
        file.write(key.export_key(format="PEM"))

def import_key(filename) -> RSA.RsaKey:
    """Import either private or public key to a directory"""
    with open(filename, "rb") as file:
        key = RSA.import_key(file.read())
    
    return key

def encrypt_message(message: bytes, public_key: RSA.RsaKey):
    """Encrypt a message using the public key"""
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message

def decrypt_message(message: bytes, private_key: RSA.RsaKey):
    """Decrypt a message using the private key"""
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(message)
    return decrypted_message.decode('utf-8')