from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class Cryptographer:
    def __init__(self, key=b'secretkey1234567', iv=b'1234567890123456', pad=b' '):

        self.key = key
        self.iv = iv
        self.pad = pad

    def encrypt_message(self, message):
        # Pad the message to a multiple of 16 bytes
        padded_message = message.encode() + (self.pad * ((16 - len(message.encode()) % 16) % 16))

        # Create an AES cipher object with the key and initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())

        # Encrypt the message using the AES cipher object
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_message) + encryptor.finalize()

        # Return the encrypted message
        return encrypted_data

    def decrypt_message(self, encrypted_data):
        # Create an AES cipher object with the key and initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())

        # Decrypt the encrypted data using the AES cipher object
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove the padding from the decrypted data
        unpadded_data = decrypted_data.rstrip(self.pad)

        # Return the decrypted message
        return unpadded_data
