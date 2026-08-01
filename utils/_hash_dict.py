
def _hash_dict(d: dict[str, str]) -> str:
    """Return a stable sha224 of a dictionary."""
    s = json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha224(s.encode("ascii")).hexdigest()

