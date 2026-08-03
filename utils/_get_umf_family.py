import copy

def _get_umf_family(A):
    """Get umfpack family string given the sparse matrix dtype."""
    _families = {
        (np.float64, np.int32): 'di',
        (np.complex128, np.int32): 'zi',
        (np.float64, np.int64): 'dl',
        (np.complex128, np.int64): 'zl'
    }

    # A.dtype.name can only be "float64" or
    # "complex128" in control flow
    f_type = getattr(np, A.dtype.name)
    # control flow may allow for more index
    # types to get through here
    i_type = getattr(np, A.indices.dtype.name)

    try:
        family = _families[(f_type, i_type)]

    except KeyError as e:
        msg = ('only float64 or complex128 matrices with int32 or int64 '
               f'indices are supported! (got: matrix: {f_type}, indices: {i_type})')
        raise ValueError(msg) from e

    # See gh-8278. Considered converting only if
    # A.shape[0]*A.shape[1] > np.iinfo(np.int32).max,
    # but that didn't always fix the issue.
    family = family[0] + "l"
    A_new = copy.copy(A)
    A_new.indptr = np.asarray(A.indptr, dtype=np.int64)
    A_new.indices = np.asarray(A.indices, dtype=np.int64)

    return family, A_new

