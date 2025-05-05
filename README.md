# imglock
imglock is a Python tool that uses Fernet encryption and steganography to hide encrypted messages inside image files. It securely embeds data in image pixels and allows for reliable extraction and decryption using a hidden key.

# imglock

**imglock** is a Python tool that combines encryption and steganography to securely hide messages inside image files. It uses Fernet encryption (AES-128 with HMAC) to encrypt data and stores it in the least significant bits of image pixels, allowing safe, covert transmission of sensitive information.

## 🔐 Features

- Generate secure Fernet keys and embed them in images.
- Encrypt messages and hide them in image files.
- Decrypt hidden messages using a key extracted from an image.
- Simple command-line interface.

## 🛠 Requirements

- Python 3.6+
- `cryptography`
- `Pillow`

Install dependencies:
pip install cryptography pillow


## 🚀 Usage

### Create a Key
python imglock.py createkey --keyfile key_image.png

### Encrypt and Hide a Message
python imglock.py encrypt --keyfile key_image.png --password "your_secret_message" --passfile target_image.png

### Extract and Decrypt a Message
python imglock.py decrypt --keyfile key_image.png --passfile target_image.png

> ⚠️ Both the key and the message are stored inside images. Make sure to back them up and protect access.

## 📁 Project Structure

- `imglock.py` – Main script for encryption, steganography, and CLI handling.
- `README.md` – Project overview and instructions.
- `LICENSE` – MIT License terms.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
