
def _dtype_to_kind(dtype_str: str) -> str:
    """
    Find the "kind" string describing the given dtype name.
    """
    if dtype_str.startswith(("string", "bytes")):
        kind = "string"
    elif dtype_str.startswith("float"):
        kind = "float"
    elif dtype_str.startswith("complex"):
        kind = "complex"
    elif dtype_str.startswith(("int", "uint")):
        kind = "integer"
    elif dtype_str.startswith("datetime64"):
        kind = dtype_str
    elif dtype_str.startswith("timedelta"):
        kind = dtype_str
    elif dtype_str.startswith("bool"):
        kind = "bool"
    elif dtype_str.startswith("category"):
        kind = "category"
    elif dtype_str.startswith("period"):
        # We store the `freq` attr so we can restore from integers
        kind = "integer"
    elif dtype_str == "object":
        kind = "object"
    elif dtype_str == "str":
        kind = "str"
    else:
        raise ValueError(f"cannot interpret dtype of [{dtype_str}]")

    return kind

