
def _mrreconstruct(subtype, baseclass, baseshape, basetype,):
    """
    Build a new MaskedArray from the information stored in a pickle.

    """
    _data = np.ndarray.__new__(baseclass, baseshape, basetype).view(subtype)
    _mask = np.ndarray.__new__(np.ndarray, baseshape, 'b1')
    return subtype.__new__(subtype, _data, mask=_mask, dtype=basetype,)

