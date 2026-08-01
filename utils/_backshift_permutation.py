
def _backshift_permutation(dim0, dim1, ndim):
    # Auxiliary function for matrix_norm
    # Computes the permutation that moves the two given dimensions to the back
    ret = [i for i in range(ndim) if i != dim0 and i != dim1]
    ret.extend((dim0, dim1))
    return ret

