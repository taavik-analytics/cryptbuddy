from Crypto.Cipher import AES, Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from key_management import encrypt_aes_key, decrypt_aes_key

def encrypt_file(file_path, public_key):
    """Encrypt a file using AES and Blowfish without external key storage."""
    # Generate a random 32-byte (256-bit) AES key
    aes_key = get_random_bytes(32)
    aes_cipher = AES.new(aes_key, AES.MODE_EAX)

    # Encrypt the file's contents using AES
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext, tag = aes_cipher.encrypt_and_digest(plaintext)

    # Encrypt the AES key using the recipient's RSA public key
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)

    # Encrypt the AES output with Blowfish
    blowfish_key = aes_key[:16]  # Use the first 16 bytes of the AES key
    blowfish_cipher = Blowfish.new(blowfish_key, Blowfish.MODE_CBC)
    blowfish_ciphertext = blowfish_cipher.encrypt(pad(ciphertext, Blowfish.block_size))

    # Save encrypted data to a new file
    with open(file_path + '.enc', 'wb') as f:
        f.write(encrypted_aes_key)     # Store RSA-encrypted AES key
        f.write(aes_cipher.nonce)      # Store AES nonce
        f.write(tag)                   # Store AES tag
        f.write(blowfish_cipher.iv)    # Store Blowfish IV
        f.write(blowfish_ciphertext)   # Store Blowfish-encrypted content

def decrypt_file(file_path, private_key):
    """Decrypt a file and return its content as a string."""
    # Read encrypted parts from the file
    with open(file_path, 'rb') as f:
        encrypted_aes_key = f.read(256)     # RSA-encrypted AES key (2048 bits = 256 bytes)
        aes_nonce = f.read(16)
        aes_tag = f.read(16)
        blowfish_iv = f.read(8)             # Blowfish IV
        blowfish_ciphertext = f.read()

    # Decrypt the AES key using the recipient's RSA private key
    aes_key = decrypt_aes_key(encrypted_aes_key, private_key)

    # Decrypt Blowfish-encrypted AES output
    blowfish_key = aes_key[:16]
    blowfish_cipher = Blowfish.new(blowfish_key, Blowfish.MODE_CBC, iv=blowfish_iv)
    aes_ciphertext = unpad(blowfish_cipher.decrypt(blowfish_ciphertext), Blowfish.block_size)

    # Decrypt the original file content using AES
    aes_cipher = AES.new(aes_key, AES.MODE_EAX, nonce=aes_nonce)
    plaintext = aes_cipher.decrypt_and_verify(aes_ciphertext, aes_tag)

    # Return the decrypted content
    return plaintext
