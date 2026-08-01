
def _recursive_printoption(result, mask, printopt):
    """
    Puts printoptions in result where mask is True.

    Private function allowing for recursion

    """
    names = result.dtype.names
    if names is not None:
        for name in names:
            curdata = result[name]
            curmask = mask[name]
            _recursive_printoption(curdata, curmask, printopt)
    else:
        np.copyto(result, printopt, where=mask)

