
def infer_method_ret_type(name: str) -> str | None:
    """Infer return types for known special methods"""
    if name.startswith("__") and name.endswith("__"):
        name = name[2:-2]
        if name in ("float", "bool", "bytes", "int", "complex", "str"):
            return name
        # Note: __eq__ and co may return arbitrary types, but bool is good enough for stubgen.
        elif name in ("eq", "ne", "lt", "le", "gt", "ge", "contains"):
            return "bool"
        elif name in ("len", "length_hint", "index", "hash", "sizeof", "trunc", "floor", "ceil"):
            return "int"
        elif name in ("format", "repr"):
            return "str"
        elif name in ("init", "setitem", "del", "delitem"):
            return "None"
    return None

