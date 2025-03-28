import rsa
from config import SECRET_PUBLIC_KEY, SECRET_PRIVATE_KEY


class Cryptography:
    public = SECRET_PUBLIC_KEY
    private = SECRET_PRIVATE_KEY

    @classmethod
    def encrypt(cls, text: str) -> bytes:
        return rsa.encrypt(text.encode(), cls.public)

    @classmethod
    def decrypt(cls, text: bytes):
        return rsa.decrypt(text, cls.private)
