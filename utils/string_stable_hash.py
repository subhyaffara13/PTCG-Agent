
def string_stable_hash(s: str) -> int:
    sha1 = hashlib.sha1(s.encode("latin1"), usedforsecurity=False).digest()
    return int.from_bytes(sha1, byteorder="little")

