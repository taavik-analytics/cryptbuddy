<img src="buddy.png" alt="CryptBuddy Logo" width="200"/>

# 🔐 CryptBuddy

CryptBuddy is a Python desktop application for encrypting, decrypting, and securely deleting files. It uses hybrid encryption combining RSA, AES, and Blowfish, wrapped in a clean and intuitive graphical interface built with Tkinter. This project was developed as a personal project for the Encryption Techniques course at Jyväskylä University of Applied Sciences in Finland.

Each user manages their friends’ public keys locally to encrypt private files for them. A more advanced key-sharing solution may be added in the future. CryptBuddy is intended for educational use only. While it uses real cryptographic algorithms, it is not suitable for high-security or production-grade applications.

---

## Features

- Automatically generates RSA key pairs on first launch
- Encrypts any file using hybrid RSA (public key) + AES + Blowfish encryption
- Smart decryption: `.txt` files are displayed directly; binary files are saved in their original format
- Secure file deletion with multiple overwrite passes
- Original file extensions are preserved (`file.pdf` → `file.pdf.enc`)

---

## Requirements

- Python 3.7 or newer

- pycryptodome

---

## How to Use

🗝️ On first run, a /keys folder will be created automatically with your RSA key pair.

### Encrypting a File

- Click “Encrypt File”

- Select the file you want to encrypt

- Choose the recipient's public_key.pem

- The encrypted file will be saved with the .enc extension

### Decrypting a File

- Click “Decrypt File”

- Choose the .enc file and your own private_key.pem

- .txt files will be displayed in a message box

- Other file types will be saved to disk

### Securely Deleting a File

- Click “Securely Delete File”

- Select a file to permanently overwrite and erase

---

MIT © Taavi Kuuluvainen