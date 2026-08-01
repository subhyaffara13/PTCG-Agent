
def dict_keys_repr(const_keys: Any, *, local: Any) -> str:
    keys_str = ",".join(const_repr(s, local=local) for s in const_keys)
    return "[" + keys_str + "]"

