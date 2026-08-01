
def hash_password(password: str) -> str:
    """Hash a password using scrypt with a random salt."""
    import base64
    import hashlib
    import os

    salt = os.urandom(16)
    dk = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    return "scrypt:" + base64.b64encode(salt + dk).decode()

