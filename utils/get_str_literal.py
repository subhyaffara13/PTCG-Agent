
def get_str_literal(v: Value) -> str | None:
    if isinstance(v, LoadLiteral) and isinstance(v.value, str):
        return v.value
    return None

