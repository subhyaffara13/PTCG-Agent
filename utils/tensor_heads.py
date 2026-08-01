
def tensor_heads(s, index_types, symmetry=None, comm=0):
    """
    Returns a sequence of TensorHeads from a string `s`
    """
    if isinstance(s, str):
        names = [x.name for x in symbols(s, seq=True)]
    else:
        raise ValueError('expecting a string')

    thlist = [TensorHead(name, index_types, symmetry, comm) for name in names]
    if len(thlist) == 1:
        return thlist[0]
    return thlist

