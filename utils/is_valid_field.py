
def is_valid_field(name: str) -> bool:
    if not name.startswith('_'):
        return True
    return ROOT_KEY == name

