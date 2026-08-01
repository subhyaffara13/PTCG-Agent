
def types_compatible(var1, var2):
    """Check if types are same or compatible.

    0-D numpy scalars are compatible with bare python scalars.
    """
    type1 = type(var1)
    type2 = type(var2)
    if type1 is type2:
        return True
    if type1 is np.ndarray and var1.shape == ():
        return type(var1.item()) is type2
    if type2 is np.ndarray and var2.shape == ():
        return type(var2.item()) is type1
    return False

