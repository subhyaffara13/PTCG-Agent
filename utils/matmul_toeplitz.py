
def matmul_toeplitz(c_or_cr, x, check_finite=False, workers=None):
    r"""Efficient Toeplitz Matrix-Matrix Multiplication using FFT.

    This function returns the matrix multiplication between a Toeplitz
    matrix and a dense matrix.

    The Toeplitz matrix has constant diagonals, with c as its first column
    and r as its first row. If r is not given, ``r == conjugate(c)`` is
    assumed.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    c_or_cr : array_like or tuple of (array_like, array_like)
        The vector ``c``, or a tuple of arrays (``c``, ``r``). If not
        supplied, ``r = conjugate(c)`` is assumed; in this case, if c[0] is
        real, the Toeplitz matrix is Hermitian. r[0] is ignored; the first row
        of the Toeplitz matrix is ``[c[0], r[1:]]``.
    x : (M,) or (M, K) array_like
        Matrix with which to multiply.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (result entirely NaNs) if the inputs do contain infinities or NaNs.
    workers : int, optional
        To pass to scipy.fft.fft and ifft. Maximum number of workers to use
        for parallel computation. If negative, the value wraps around from
        ``os.cpu_count()``. See scipy.fft.fft for more details.

    Returns
    -------
    T @ x : (M,) or (M, K) ndarray
        The result of the matrix multiplication ``T @ x``. Shape of return
        matches shape of `x`.

    See Also
    --------
    toeplitz : Toeplitz matrix
    solve_toeplitz : Solve a Toeplitz system using Levinson Recursion

    Notes
    -----
    The Toeplitz matrix is embedded in a circulant matrix and the FFT is used
    to efficiently calculate the matrix-matrix product.

    Because the computation is based on the FFT, integer inputs will
    result in floating point outputs.  This is unlike NumPy's `matmul`,
    which preserves the data type of the input.

    This is partly based on the implementation that can be found in [1]_,
    licensed under the MIT license. More information about the method can be
    found in reference [2]_. References [3]_ and [4]_ have more reference
    implementations in Python.

    .. versionadded:: 1.6.0

    References
    ----------
    .. [1] Jacob R Gardner, Geoff Pleiss, David Bindel, Kilian
       Q Weinberger, Andrew Gordon Wilson, "GPyTorch: Blackbox Matrix-Matrix
       Gaussian Process Inference with GPU Acceleration" with contributions
       from Max Balandat and Ruihan Wu. Available online:
       https://github.com/cornellius-gp/gpytorch

    .. [2] J. Demmel, P. Koev, and X. Li, "A Brief Survey of Direct Linear
       Solvers". In Z. Bai, J. Demmel, J. Dongarra, A. Ruhe, and H. van der
       Vorst, editors. Templates for the Solution of Algebraic Eigenvalue
       Problems: A Practical Guide. SIAM, Philadelphia, 2000. Available at:
       http://www.netlib.org/utk/people/JackDongarra/etemplates/node384.html

    .. [3] R. Scheibler, E. Bezzam, I. Dokmanic, Pyroomacoustics: A Python
       package for audio room simulations and array processing algorithms,
       Proc. IEEE ICASSP, Calgary, CA, 2018.
       https://github.com/LCAV/pyroomacoustics/blob/pypi-release/
       pyroomacoustics/adaptive/util.py

    .. [4] Marano S, Edwards B, Ferrari G and Fah D (2017), "Fitting
       Earthquake Spectra: Colored Noise and Incomplete Data", Bulletin of
       the Seismological Society of America., January, 2017. Vol. 107(1),
       pp. 276-291.

    Examples
    --------
    Multiply the Toeplitz matrix T with matrix x::

            [ 1 -1 -2 -3]       [1 10]
        T = [ 3  1 -1 -2]   x = [2 11]
            [ 6  3  1 -1]       [2 11]
            [10  6  3  1]       [5 19]

    To specify the Toeplitz matrix, only the first column and the first
    row are needed.

    >>> import numpy as np
    >>> c = np.array([1, 3, 6, 10])    # First column of T
    >>> r = np.array([1, -1, -2, -3])  # First row of T
    >>> x = np.array([[1, 10], [2, 11], [2, 11], [5, 19]])

    >>> from scipy.linalg import toeplitz, matmul_toeplitz
    >>> matmul_toeplitz((c, r), x)
    array([[-20., -80.],
           [ -7.,  -8.],
           [  9.,  85.],
           [ 33., 218.]])

    Check the result by creating the full Toeplitz matrix and
    multiplying it by ``x``.

    >>> toeplitz(c, r) @ x
    array([[-20, -80],
           [ -7,  -8],
           [  9,  85],
           [ 33, 218]])

    The full matrix is never formed explicitly, so this routine
    is suitable for very large Toeplitz matrices.

    >>> n = 1000000
    >>> matmul_toeplitz([1] + [0]*(n-1), np.ones(n))
    array([1., 1., 1., ..., 1., 1., 1.], shape=(1000000,))

    """

    from ..fft import fft, ifft, rfft, irfft
    c, r = c_or_cr if isinstance(c_or_cr, tuple) else (c_or_cr, np.conjugate(c_or_cr))

    return _matmul_toepltiz(r, c, x, workers, check_finite, fft, ifft, rfft, irfft)

