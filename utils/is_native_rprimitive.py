
def is_native_rprimitive(rtype: RType) -> bool:
    return isinstance(rtype, RPrimitive) and rtype.name in KNOWN_NATIVE_TYPES

