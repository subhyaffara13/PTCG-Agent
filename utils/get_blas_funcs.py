
def get_blas_funcs(names, arrays=(), dtype=None, ilp64="preferred"):
    """Return available BLAS function objects from names.

    Arrays are used to determine the optimal prefix of BLAS routines.

    Parameters
    ----------
    names : str or sequence of str
        Name(s) of BLAS functions without type prefix.

    arrays : sequence of ndarrays, optional
        Arrays can be given to determine optimal prefix of BLAS
        routines. If not given, double-precision routines will be
        used, otherwise the most generic type in arrays will be used.

    dtype : str or dtype, optional
        Data-type specifier. Not used if `arrays` is non-empty.

    ilp64 : {True, False, 'preferred'}, optional
        Whether to return ILP64 routine variant.
        Choosing ``'preferred'`` returns ILP64 routine if available,
        and otherwise the 32-bit (LP64) routine. Default: ``'preferred'``.

    Returns
    -------
    funcs : list
        List containing the found function(s).

    Raises
    ------
    RuntimeError
        If the requested LP64/ILP64 variant is not available.

    See Also
    --------
    scipy.linalg.lapack.get_lapack_funcs
        a similar routine for selecting LAPACK functions.

    Notes
    -----
    In BLAS, the naming convention is that all functions start with a
    type prefix, which depends on the type of the principal
    matrix. These can be one of ``{'s', 'd', 'c', 'z'}`` for the NumPy
    types ``{float32, float64, complex64, complex128}`` respectively.
    The code and the dtype are stored in attributes `typecode` and `dtype`
    of the returned functions.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy.linalg as LA
    >>> rng = np.random.default_rng()
    >>> a = rng.random((3, 2))
    >>> x_gemv = LA.get_blas_funcs('gemv', (a,))

    Note that ``x_gemv`` string representation shows the exact BLAS function with the
    prefix (here, ``d-`` because ``a`` is double precision real):

    >>> x_gemv
    <fortran function dgemv>

    The BLAS variant information is also available from the ``typecode`` attribute:

    >>> x_gemv.typecode
    'd'

    For double precision complex arrays, we select the ``z-`` variant, ``zgemv``

    >>> x_gemv = LA.get_blas_funcs('gemv', (a*1j,))
    >>> x_gemv.typecode
    'z'

    If you want to select a specific BLAS variant instead of relying on array types, use
    the ``dtype=`` argument:

    >>> LA.get_blas_funcs('gemv', dtype=np.float32)
    <fortran function sgemv>

    The ``int_dtype`` attribute stores whether the routine is ILP64 (integer arguments
    and outputs are 64-bit) or LP64 (integer arguments and outputs are 32-bit):

    >>> x_gemv.int_dtype
    dtype('int32')   # may vary
    """
    if isinstance(ilp64, str):
        if ilp64 == 'preferred':
            ilp64 = HAS_ILP64
        else:
            raise ValueError(f"Invalid value for {ilp64 = }.")

    if not ilp64:
        return _get_funcs(
            names, arrays, dtype, "BLAS", _fblas, "fblas", _blas_alias, ilp64=False
        )
    else:
        if not HAS_ILP64:
            raise RuntimeError("BLAS ILP64 routine requested, but Scipy "
                               "compiled only with 32-bit BLAS")
        return _get_funcs(
            names, arrays, dtype, "BLAS", _fblas_64, "fblas_64", _blas_alias, ilp64=True
        )

