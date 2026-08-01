
def find_best_blas_type(arrays=(), dtype=None):
    """Find best-matching BLAS/LAPACK type.

    Arrays are used to determine the optimal prefix of BLAS routines.

    Parameters
    ----------
    arrays : sequence of ndarrays, optional
        Arrays can be given to determine optimal prefix of BLAS
        routines. If not given, double-precision routines will be
        used, otherwise the most generic type in arrays will be used.
    dtype : str or dtype, optional
        Data-type specifier. Not used if `arrays` is non-empty.

    Returns
    -------
    prefix : str
        BLAS/LAPACK prefix character.
    dtype : dtype
        Inferred Numpy data type.
    prefer_fortran : bool
        Whether to prefer Fortran order routines over C order.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy.linalg.blas as bla
    >>> rng = np.random.default_rng()
    >>> a = rng.random((10,15))
    >>> b = np.asfortranarray(a)  # Change the memory layout order
    >>> bla.find_best_blas_type((a,))
    ('d', dtype('float64'), False)
    >>> bla.find_best_blas_type((a*1j,))
    ('z', dtype('complex128'), False)
    >>> bla.find_best_blas_type((b,))
    ('d', dtype('float64'), True)

    """
    dtype = np.dtype(dtype)
    max_score = _type_score.get(dtype.char, 5)
    prefer_fortran = False

    if arrays:
        # In most cases, single element is passed through, quicker route
        if len(arrays) == 1:
            max_score = _type_score.get(arrays[0].dtype.char, 5)
            prefer_fortran = arrays[0].flags['FORTRAN']
        else:
            # use the most generic type in arrays
            scores = [_type_score.get(x.dtype.char, 5) for x in arrays]
            max_score = max(scores)
            ind_max_score = scores.index(max_score)
            # safe upcasting for mix of float64 and complex64 --> prefix 'z'
            if max_score == 3 and (2 in scores):
                max_score = 4

            if arrays[ind_max_score].flags['FORTRAN']:
                # prefer Fortran for leading array with column major order
                prefer_fortran = True

    # Get the LAPACK prefix and the corresponding dtype if not fall back
    # to 'd' and double precision float.
    prefix, dtype = _type_conv.get(max_score, ('d', np.dtype('float64')))

    return prefix, dtype, prefer_fortran

