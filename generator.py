import argparse
import hashlib as _hashlib
import hmac
import string
import secrets
import sys
from base64 import b64encode, b64decode

from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad


class Generator:
    nonce_size_bytes = 64
    enc_func_iv_bytes = {
        "3des": 8,
        "aes128": 16,
        "aes192": 16,
        "aes256": 16
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
        if type(password) == str:
            self.password = bytearray.fromhex(password)
        else:
            self.password = bytearray(password)
            password = password.decode()
        self.hash_func = hash_func
        self.nonce = self.gen_nonce()
        self.enc_func = enc_func
        self.iv = self.gen_iv()
        self.filename = hash_func + "_" + enc_func + "_" + password + ".enc"

    def generate(self):
        key = self.hmac()
        self.enc_and_fill_file(key)

    def enc(self, key, text):
        #c_text = bytearray(8)
        #c_text.extend(text)
        if self.enc_func.__eq__("3des"):
            cipher = DES3.new(key, DES3.MODE_CBC, self.iv)
        else:
            cipher = AES.new(key, DES3.MODE_CBC, self.iv)
        return cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))

    def dec(self, key, text):
        if self.enc_func.__eq__("3des"):
            cipher = DES3.new(key, DES3.MODE_CBC, self.iv)
        else:
            cipher = AES.new(key, DES3.MODE_CBC, self.iv)
        return cipher.decrypt(text)

    def gen_nonce(self):
        result = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase)
                         for i in range(self.nonce_size_bytes))
        return result.encode()

    def gen_iv(self):
        result = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase)
                         for i in range(self.enc_func_iv_bytes.get(self.enc_func)))
        return result.encode()

    def hmac(self):
        key_len = self.enc_func_key_bytes.get(self.enc_func)
        key = self.gen_key()
        if len(key) < key_len:
            key.extend(self.gen_key())
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
        text = open("input.txt", "r").readline()
        hash_bin = bin(int(self.hash_func_id.get(self.hash_func), base=16))[2:].zfill(2)
        enc_bin = bin(int(self.enc_func_id.get(self.enc_func), base=16))[2:].zfill(2)
        output.write("ENC" + hash_bin + enc_bin)
        nonce_bin = bin(int(self.nonce.hex(), base=16))[2:].zfill(8*self.nonce_size_bytes)
        iv_bin = bin(int(self.iv.hex(), base=16))[2:].zfill(8*self.enc_func_iv_bytes.get(self.enc_func))
        output.write(nonce_bin)
        output.write(iv_bin)
        res = self.enc(key, text)
        final_len = len(res)*8
        res_bin = bin(int(res.hex(), base=16))[2:].zfill(final_len)
        print(int(res_bin, base=2).to_bytes(len(res_bin)//8, 'big', signed=False).hex())
        output.write(res_bin)
        output.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--password',
                        action='store',
                        type=str,
                        required=True,
                        help='enter password - 4 bytes')
    parser.add_argument('--hash',
                        action='store',
                        type=str,
                        required=True,
                        help='enter hash-function name',
                        choices=['md5', 'sha1'])
    parser.add_argument('-a',
                        '--algo',
                        action='store',
                        required=True,
                        type=str,
                        help='enter enc-function name',
                        choices=['3des', 'aes128', 'aes192', 'aes256'])
    args = parser.parse_args()
    gen = Generator(args.password, args.hash, args.algo)
    gen.generate()
