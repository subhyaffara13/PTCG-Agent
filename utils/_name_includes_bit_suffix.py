
def _name_includes_bit_suffix(dtype):
    if dtype.type == np.object_:
        # pointer size varies by system, best to omit it
        return False
    elif dtype.type == np.bool:
        # implied
        return False
    elif dtype.type is None:
        return True
    elif np.issubdtype(dtype, np.flexible) and _isunsized(dtype):
        # unspecified
        return False
    else:
        return True

