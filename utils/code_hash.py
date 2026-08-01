
def code_hash(code: str | bytes, extra: str | bytes = "") -> str:
    hashing_str = code if isinstance(code, bytes) else code.encode("utf-8")
    if extra:
        extra_b = extra if isinstance(extra, bytes) else extra.encode("utf-8")
        hashing_str = hashing_str + b"||" + extra_b
    return "c" + sha256_hash(hashing_str)

