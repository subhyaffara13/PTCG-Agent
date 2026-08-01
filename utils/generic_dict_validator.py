
def genericDictValidator(value: Any, prototype: GenericDict) -> bool:
    """
    Generic. (Added at version 3.)
    """
    # not a dict
    if not isinstance(value, Mapping):
        return False
    # missing required keys
    for key, (typ, required) in prototype.items():
        if not required:
            continue
        if key not in value:
            return False
    # unknown keys
    for key in value.keys():
        if key not in prototype:
            return False
    # incorrect types
    for key, v in value.items():
        prototypeType, required = prototype[key]
        if v is None and not required:
            continue
        if not isinstance(v, prototypeType):
            return False
    return True

