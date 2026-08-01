
def _hash_content(s: str):
    return hashlib.sha256(s.strip().encode("utf-8")).hexdigest()

