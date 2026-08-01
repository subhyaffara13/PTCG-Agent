
def verify_password(password: str, stored: str) -> bool:
    """Verify a password against a stored hash. Supports scrypt and SHA256."""
    import base64
    import hashlib
    import secrets

    if stored.startswith("scrypt:"):
        try:
            raw = base64.b64decode(stored[7:])
            salt, dk = raw[:16], raw[16:]
            dk2 = hashlib.scrypt(
                password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32
            )
            return secrets.compare_digest(dk, dk2)
        except Exception:
            return False
    # SHA256 fallback (not vulnerable to pass-the-hash: checks sha256(input) == stored)
    if len(stored) == 64 and all(c in "0123456789abcdef" for c in stored):
        return secrets.compare_digest(
            hashlib.sha256(password.encode()).hexdigest().encode(), stored.encode()
        )
    return False

