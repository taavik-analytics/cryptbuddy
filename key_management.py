import random
import string
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_keys():
    """Generate an RSA key pair."""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_aes_key(aes_key, public_key):
    """Encrypt an AES key using the recipient's RSA public key."""
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_aes_key = rsa_cipher.encrypt(aes_key)
    return encrypted_aes_key

def decrypt_aes_key(encrypted_aes_key, private_key):
    """Decrypt an AES key using the recipient's RSA private key."""
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    aes_key = rsa_cipher.decrypt(encrypted_aes_key)
    return aes_key
