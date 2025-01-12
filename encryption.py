from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import base64
import os

class AESHandler:
    @staticmethod
    def generate_key():
        return get_random_bytes(16)

    @staticmethod
    def encrypt_text(key, text):
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode()

    @staticmethod
    def decrypt_text(key, encrypted_text):
        encrypted_data = base64.b64decode(encrypted_text)
        iv = encrypted_data[:AES.block_size]
        ct = encrypted_data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    @staticmethod
    def encrypt_file(key, file_path):
        with open(file_path, "rb") as input_file:
            input_data = input_file.read()
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(input_data, AES.block_size))
        encrypted_data = cipher.iv + ct_bytes

        encrypted_file_path = f"{file_path}.enc"
        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        return encrypted_file_path

    @staticmethod
    def decrypt_file(key, file_path):
        with open(file_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        iv = encrypted_data[:AES.block_size]
        ct = encrypted_data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        original_data = unpad(cipher.decrypt(ct), AES.block_size)

        original_ext = os.path.splitext(file_path.replace(".enc", ""))[1] or ".jpg"
        decrypted_file_path = file_path.replace(".enc", f"_decrypted{original_ext}")
        with open(decrypted_file_path, "wb") as decrypted_file:
            decrypted_file.write(original_data)
        return decrypted_file_path