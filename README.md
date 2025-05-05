# imglock

**imglock** is a secure, image-based password manager. It encrypts your passwords using Fernet symmetric encryption and hides them inside images using steganography. Your credentials are protected and disguised — visible only to those with the right key image.

## 🔐 Why imglock?

Unlike traditional password managers that store sensitive data in vault files, **imglock** hides encrypted passwords inside images. This reduces the risk of detection and makes your password storage both secure and covert.

## ✨ Features

- Secure AES-128 encryption with HMAC authentication (via Fernet).
- Passwords are hidden inside image pixels using LSB steganography.
- Easily store and retrieve credentials with two images: one as the key, one as the password container.
- Lightweight, offline, and open source.

## 🛠 Requirements

- Python 3.6+
- `cryptography`
- `Pillow`

Install dependencies:
pip install cryptography pillow

## 🚀 Usage

### Step 1: Create a Key Image
This image will store your encryption key:
python imglock.py createkey --keyfile key_image.png

### Step 2: Encrypt and Hide a Password
This embeds an encrypted password in a cover image:
python imglock.py encrypt --keyfile key_image.png --password "My$ecretP@ssw0rd" --passfile password_image.png

### Step 3: Extract and Decrypt the Password
This recovers the original password using the key image:
python imglock.py decrypt --keyfile key_image.png --passfile password_image.pngc

> 🛡️ Both the key and password image are needed to access the stored credentials. Keep them secure!

## 📁 Project Structure

- `imglock.py` – Core CLI and logic for encryption, embedding, and recovery.
- `README.md` – Project documentation.
- `LICENSE` – MIT License file.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
