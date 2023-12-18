import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def hash_password(password: str) -> str:
    """Hash (password + salt)"""
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    return hashed_pass.decode()

def check_password(password: bytes, hashed_password: bytes) -> bool:
    """Check if password matches hash(password + salt)"""
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False

# public key used for encrypting, private key used for decrypting (confidentiality)
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

def encrypt_message(message: bytes, public_key: RSA.RsaKey) -> bytes:
    """Encrypt a message using the public key, returns encrypted bytes"""
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message

def decrypt_message(message: bytes, private_key: RSA.RsaKey, format: str) -> str:
    """Decrypt a message using the private key, returns decrypted str"""
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(message)
    return decrypted_message.decode(format)

def sign_message(message, private_key: RSA.RsaKey):
    """Sign message using sender's private key"""
    hash = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(hash)

    return signature

def verify_sign(message, signature, public_key: RSA.RsaKey):
    """Verify message using sender's public key"""
    hash = SHA256.new(message)
    try:
        pkcs1_15.new(public_key).verify(hash, signature)
        return True
    except (ValueError, TypeError):
        return False
