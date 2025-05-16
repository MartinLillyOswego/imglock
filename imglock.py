from cryptography.fernet import Fernet
import argparse
from PIL import Image

def encrypt(message, key) -> bytes:
    return Fernet(key).encrypt(message.encode())

def decrypt(key, password) -> str:
    return Fernet(key).decrypt(password).decode()

def message_to_bits(message: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in message)

def bits_to_bytes(bits: str) -> bytes:
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def encode_image(image_path, message_bytes):
    img = Image.open(image_path)
    img = img.convert('RGB')  # ensure RGB
    pixels = img.load()
    width, height = img.size

    # Step 1: Encode the length of the message (in bytes) as 32 bits
    message_length = len(message_bytes)
    length_bits = f'{message_length:032b}'

    # Step 2: Encode the message as bits
    message_bits = message_to_bits(message_bytes)

    # Combine length and message
    full_bits = length_bits + message_bits

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(full_bits):
                img.save(image_path)
                print(f"Message encoded and saved to {image_path}")
                return
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(full_bits[bit_index])  # modify LSB of red
            bit_index += 1
            pixels[x, y] = (r, g, b)

    raise ValueError("Image too small to hold the message.")

def extract_hidden_bytes(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)

            if len(bits) >= 32:
                message_length = int(bits[:32], 2)  # First 32 bits = length
                total_bits = 32 + message_length * 8

                if len(bits) >= total_bits:
                    message_bits = bits[32:total_bits]
                    return bits_to_bytes(message_bits)

    raise ValueError("No hidden message found or image was truncated.")

if __name__ == "__main__":
    import sys

    # First, parse only the 'mode' argument
    mode_parser = argparse.ArgumentParser(add_help=False)
    mode_parser.add_argument("mode", choices=["encrypt", "decrypt", "createkey"])
    known_args, remaining_args = mode_parser.parse_known_args()

    # Now build the full parser
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a message.")
    parser.add_argument("mode", choices=["encrypt", "decrypt", "createkey"], help="Mode to run in.")
    parser.add_argument("--password", help="Password for key generation.")
    parser.add_argument("--passfile", help="Message to encrypt or decrypt.")
    parser.add_argument("--keyfile", help="Key file to use for encrypt/decrypt (optional)")

    args = parser.parse_args()

    if args.mode == "encrypt":
        if not args.keyfile:
            print("keyfile argument is required for encryption.")
            exit(1)
        if not args.password:
            print("Password argument is required for encryption.")
            exit(1)
        if not args.passfile:
            print("passfile argument is required for encryption.")
            exit(1)

        key = extract_hidden_bytes(args.keyfile)

        encoded_password = encrypt(args.password, key)

        encode_image(args.passfile, encoded_password)

        print(f"password: ({args.password}) encoded into image {args.passfile}")
        
    elif args.mode == "decrypt":
        if not args.keyfile:
            print("keyfile argument is required for decryption.")
            exit(1)
        if not args.passfile:
            print("Passfile argument is required for decryption.")
            exit(1)

        key = extract_hidden_bytes(args.keyfile)
        password = extract_hidden_bytes(args.passfile)

        decrypted_message = decrypt(key, password)
        print(f"Decrypted message: {decrypted_message}")
   
    elif args.mode == "createkey":
        # Generate a new key
        key = Fernet.generate_key()

        if args.keyfile:
            encode_image(args.keyfile, key)
            print(f"Key: ({str(key)}) encoded into image {args.keyfile}")

        else:
            print("keyfile argument is required for key creation.")





