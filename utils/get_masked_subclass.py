
def get_masked_subclass(*arrays):
    """
    Return the youngest subclass of MaskedArray from a list of (masked) arrays.

    In case of siblings, the first listed takes over.

    """
    if len(arrays) == 1:
        arr = arrays[0]
        if isinstance(arr, MaskedArray):
            rcls = type(arr)
        else:
            rcls = MaskedArray
    else:
        arrcls = [type(a) for a in arrays]
        rcls = arrcls[0]
        if not issubclass(rcls, MaskedArray):
            rcls = MaskedArray
        for cls in arrcls[1:]:
            if issubclass(cls, rcls):
                rcls = cls
    # Don't return MaskedConstant as result: revert to MaskedArray
    if rcls.__name__ == 'MaskedConstant':
        return MaskedArray
    return rcls

