
def is_valid_privateattr_name(name: str) -> bool:
    return name.startswith('_') and not name.startswith('__')

