
def compute_hash(text: str) -> str:
    # We use a crypto hash instead of the builtin hash(...) function
    # because the output of hash(...)  can differ between runs due to
    # hash randomization (enabled by default in Python 3.3).  See the
    # note in
    # https://docs.python.org/3/reference/datamodel.html#object.__hash__.
    return hash_digest(text.encode("utf-8"))

