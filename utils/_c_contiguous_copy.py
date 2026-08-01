
def _C_contiguous_copy(A):
    """
    Same as np.ascontiguousarray, but ensure a copy
    """
    A = np.asarray(A)
    if A.flags.c_contiguous:
        A = A.copy()
    else:
        A = np.ascontiguousarray(A)
    return A

