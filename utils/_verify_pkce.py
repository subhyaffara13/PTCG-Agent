
def _verify_pkce(code_verifier: str, code_challenge: str) -> bool:
    """Return True iff SHA-256(code_verifier) == code_challenge (base64url, no padding)."""
    digest = hashlib.sha256(code_verifier.encode()).digest()
    computed = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return computed == code_challenge

