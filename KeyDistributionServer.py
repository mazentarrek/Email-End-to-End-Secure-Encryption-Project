import socket
import threading
from Crypto.Cipher import AES
from Cryptodome.Util.Padding import pad

from Encrypt_Decrypt import *
import secrets

# Read the keys from the files
with open('key_master_a.txt', 'rb') as f:
    key_master_a = f.read()

with open('key_master_b.txt', 'rb') as f:
    key_master_b = f.read()

class KeyDistributionServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.users = {}

    @staticmethod
    def generate_random_key():
        key_length = 16  # 16 bytes (128 bits)
        random_bytes = secrets.token_bytes(key_length)
        return bytes(random_bytes)

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

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Key Distribution Server started on {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} \n")

    def handle_client(self, client_socket, client_address):
        print(f"[NEW CONNECTION] {client_address} connected.")

        self.handle_key_request(client_socket)

        print(f"[CONNECTION CLOSING] {client_address} closed.")
        client_socket.close()
    def handle_key_request(self, client_socket):

        sessionkey = self.generate_random_key()

        print(f"Session Key generated is: {sessionkey}")

        encrypted_session_key_a = encrypt_key(sessionkey, key_master_a)
        encrypted_session_key_b = encrypt_key(sessionkey, key_master_b)

        client_socket.send(encrypted_session_key_a)
        client_socket.send(encrypted_session_key_b)


# Example usage
if __name__ == "__main__":
    server = KeyDistributionServer('localhost', 5000)
    server.run()