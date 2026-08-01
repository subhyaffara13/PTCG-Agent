
def _immutable_dict(items):
    """
    Creates a mapping where items cannot be added, deleted, or updated.
    NOTE: The immutability is shallow (like tuple is an immutable collection).
    """
    from types import MappingProxyType

    return MappingProxyType(dict(items))

