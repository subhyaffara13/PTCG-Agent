
def extract_var_from_literal_hash(key: Key) -> Var | None:
    """If key refers to a Var node, return it.

    Return None otherwise.
    """
    if len(key) == 2 and key[0] == "Var" and isinstance(key[1], Var):
        return key[1]
    return None

