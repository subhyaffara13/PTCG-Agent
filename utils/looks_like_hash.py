
def looks_like_hash(sha: str) -> bool:
    return bool(HASH_REGEX.match(sha))

