import hashlib as _hashlib
import hmac
from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES3, AES


class Generator:
    nonce_size_bytes = 64
    enc_func_iv_bytes = {
        "3des": 8,
        "aes128": 16,
        "aes192": 24,
        "aes256": 32
    }
    enc_func_key_bytes = {
        "3des": 24,
        "aes128": 16,
        "aes192": 24,
        "aes256": 32
    }
    enc_func_id = {
        "3des": "0",
        "aes128": "1",
        "aes192": "2",
        "aes256": "3"
    }
    hash_func_id = {
        "md5": "0",
        "sha1": "1"
    }

    def get_iv_bytes(self, enc_f):
        return self.enc_func_iv_bytes.get(enc_f)

    def __init__(self, password, hash_func, enc_func):
        self.password = bytearray.fromhex(password)
        self.hash_func = hash_func
        self.nonce = self.gen_nonce()
        self.iv = bytearray()
        self.enc_func = enc_func
        self.filename = hash_func + "_" + enc_func + "_" + password + ".enc"

    def generate(self):
        key = self.hmac()
        self.enc_and_fill_file(key)

    def enc(self, key, text):
        c_text = bytearray(8)
        c_text.extend(text)
        if self.enc_func.__eq__("3des"):
            cipher = DES3.new(key, DES3.MODE_CBC)
        else:
            cipher = AES.new(key, DES3.MODE_CBC)
        self.iv = cipher.iv
        return cipher.iv.hex() + cipher.encrypt(c_text).hex()

    def dec(self, key, text):
        if self.enc_func.__eq__("3des"):
            cipher = DES3.new(key, DES3.MODE_CBC, self.iv)
        else:
            cipher = AES.new(key, DES3.MODE_CBC, self.iv)
        return cipher.decrypt(text)

    def gen_nonce(self):
        return get_random_bytes(self.nonce_size_bytes)

    def hmac(self):
        key_len = self.enc_func_key_bytes.get(self.enc_func)
        key = self.gen_key()
        if len(key) < key_len:
            key.extend(self.gen_key(key))
        return key[:key_len]

    def gen_key(self):
        if self.hash_func.__eq__("md5"):
            func = _hashlib.md5
        else:
            func = _hashlib.sha1
        digest = hmac.new(key=self.password, msg=self.nonce, digestmod=func).hexdigest()
        return bytearray.fromhex(digest)

    def create_file(self):
        return open(self.filename, "w")

    def enc_and_fill_file(self, key):
        output = self.create_file()
        text = bytearray.fromhex(open("input.txt", "r").readline())
        output.write("ENC" + self.hash_func_id.get(self.hash_func) + self.enc_func_id.get(self.enc_func))
        output.write(self.nonce.hex())
        print(self.nonce.hex().__len__())
        output.write(self.enc(key, text))
        output.close()
