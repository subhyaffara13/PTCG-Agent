
def is_erased_instance(t: Instance) -> bool:
    """Is this an instance where all args are Any types?"""
    if not t.args:
        return False
    for arg in t.args:
        if isinstance(arg, UnpackType):
            unpacked = get_proper_type(arg.type)
            if not isinstance(unpacked, Instance):
                return False
            assert unpacked.type.fullname == "builtins.tuple"
            if not isinstance(get_proper_type(unpacked.args[0]), AnyType):
                return False
        elif not isinstance(get_proper_type(arg), AnyType):
            return False
    return True

