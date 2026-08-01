
def is_complex_type(dtype):
    return np.dtype(dtype).kind == "c"


def isComplexType(t):
    return issubclass(t, complexfloating)

