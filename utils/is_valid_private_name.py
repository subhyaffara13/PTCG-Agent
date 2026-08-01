
def is_valid_private_name(name: str) -> bool:
    return not is_valid_field(name) and name not in DUNDER_ATTRIBUTES

