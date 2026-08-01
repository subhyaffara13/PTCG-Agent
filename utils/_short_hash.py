
def _short_hash(filename: str) -> str:
    return base64.urlsafe_b64encode(hashlib.sha1(filename.encode()).digest()).decode()

