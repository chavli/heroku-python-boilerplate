"""
    original author and code:
    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

    adapted for Python3
"""
import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES


class AESCipher(object):
    """ wrapper around Crypto that makes it easy to encrypt and decrypt data """

    def __init__(self, key: str):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw: str) -> bytes:
        """ encrypt a given string. returns a base64 encoded bytes object """

        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8")))

    def decrypt(self, enc: bytes) -> str:
        """ decrypt a given base64 bytes object. returns a string """
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")

    def _pad(self, s: str) -> str:
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
