
def _hash_cli_sso_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()

