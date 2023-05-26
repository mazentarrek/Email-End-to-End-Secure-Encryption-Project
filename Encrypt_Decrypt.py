import os, random, struct
from Cryptodome.Cipher import AES
from secrets import token_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# Generate a random IV
iv = b"5678123456781234"
def encrypt_file(key, in_filename, out_filename=None, chunksize=16):
    """ Encrypts a file using AES (CBC mode) with the
    given key.
    key:
    The encryption key - a string that must be
    either 16, 24 or 32 bytes long. Longer keys
    are more secure.
    in_filename:
    Name of the input file
    out_filename:
    If None, '<in_filename>.enc' will be used.
    chunksize:
    Sets the size of the chunk which the function
    uses to read and encrypt the file. Larger chunk
    sizes can be faster for some files and machines.
    chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=16):
    """ Decrypts a file using AES (CBC mode) with the
    given key. Parameters are similar to encrypt_file,
    with one difference: out_filename, if not supplied
    will be in_filename without its last extension
    (i.e. if in_filename is 'aaa.zip.enc' then
    out_filename will be 'aaa.zip')
    """

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:

        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

def generate_random_key():
    """
    Generates a random 16-byte number and returns it as a byte string in the format b"1234567812345678".

    Returns:
        bytes: The randomly generated key.
    """
    random_bytes = bytes(random.randint(0, 255) for _ in range(16))  # Generate 16 random bytes
    key = random_bytes

    return key

def encrypt_key(message: bytes, key: bytes) -> bytes:
    # Create an AES cipher object with the key and a random initialization vector (IV)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    # Pad the message to make it a multiple of the block size and encode it as bytes
    padded_message = pad(message, AES.block_size)

    # Encrypt the padded message
    encrypted_message = cipher.encrypt(padded_message)

    # Return the IV and encrypted message
    return iv + encrypted_message

def decrypt_key(encrypted_message: bytes, key: bytes) -> str:
    # Extract the initialization vector (IV) from the encrypted message
    iv = encrypted_message[:AES.block_size]
    encrypted_message = encrypted_message[AES.block_size:]

    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the encrypted message
    decrypted_message = cipher.decrypt(encrypted_message)

    # Unpad the decrypted message and decode it as a string
    unpadded_message = unpad(decrypted_message, AES.block_size)
    message = unpadded_message

    # Return the decrypted message
    return message

def encrypt_message(message: str, key: bytes) -> bytes:
    # Create an AES cipher object with the key and a random initialization vector (IV)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    # Pad the message to make it a multiple of the block size and encode it as bytes
    padded_message = pad(message.encode(), AES.block_size)

    # Encrypt the padded message
    encrypted_message = cipher.encrypt(padded_message)

    # Return the IV and encrypted message
    return iv + encrypted_message

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    # Extract the initialization vector (IV) from the encrypted message
    iv = encrypted_message[:AES.block_size]
    encrypted_message = encrypted_message[AES.block_size:]

    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the encrypted message
    decrypted_message = cipher.decrypt(encrypted_message)

    # Unpad the decrypted message and decode it as a string
    unpadded_message = unpad(decrypted_message, AES.block_size)
    message = unpadded_message.decode()

    # Return the decrypted message
    return message
