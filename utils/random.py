from typing import Any

def random(mode: str = "RGB") -> ImagePalette:
    from random import randint

    palette = [randint(0, 255) for _ in range(256 * len(mode))]
    return ImagePalette(mode, palette)


def random(m, n, density=0.01, format='coo', dtype=None,
           rng=None, data_rvs=None):
    """Generate a sparse matrix of the given shape and density with randomly
    distributed values.

    .. warning::

        This function returns a sparse matrix -- not a sparse array.
        You are encouraged to use `random_array` to take advantage of the
        sparse array functionality.

    Parameters
    ----------
    m, n : int
        shape of the matrix
    density : real, optional
        density of the generated matrix: density equal to one means a full
        matrix, density of 0 means a matrix with no non-zero items.
    format : str, optional
        sparse matrix format.
    dtype : dtype, optional
        type of the returned matrix values.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

        This random state will be used for sampling the sparsity structure, but
        not necessarily for sampling the values of the structurally nonzero
        entries of the matrix.
    data_rvs : callable, optional
        Samples a requested number of random values.
        This function should take a single argument specifying the length
        of the ndarray that it will return. The structurally nonzero entries
        of the sparse random matrix will be taken from the array sampled
        by this function. By default, uniform [0, 1) random values will be
        sampled using the same random state as is used for sampling
        the sparsity structure.

    Returns
    -------
    res : sparse matrix
        Random sparse matrix.

    See Also
    --------
    random_array : constructs sparse arrays instead of sparse matrices

    Examples
    --------

    Passing a ``np.random.Generator`` instance for better performance:

    >>> import scipy as sp
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> S = sp.sparse.random(3, 4, density=0.25, rng=rng)

    Providing a sampler for the values:

    >>> rvs = sp.stats.poisson(25, loc=10).rvs
    >>> S = sp.sparse.random(3, 4, density=0.25, rng=rng, data_rvs=rvs)
    >>> S.toarray()
    array([[ 36.,   0.,  33.,   0.],   # random
           [  0.,   0.,   0.,   0.],
           [  0.,   0.,  36.,   0.]])

    Building a custom distribution.
    This example builds a squared normal from np.random:

    >>> def np_normal_squared(size=None, rng=rng):
    ...     return rng.standard_normal(size) ** 2
    >>> S = sp.sparse.random(3, 4, density=0.25, rng=rng,
    ...                      data_rvs=np_normal_squared)

    Or we can build it from sp.stats style rvs functions:

    >>> def sp_stats_normal_squared(size=None, rng=rng):
    ...     std_normal = sp.stats.distributions.norm_gen().rvs
    ...     return std_normal(size=size, random_state=rng) ** 2
    >>> S = sp.sparse.random(3, 4, density=0.25, rng=rng,
    ...                      data_rvs=sp_stats_normal_squared)

    Or we can subclass sp.stats rv_continuous or rv_discrete:

    >>> class NormalSquared(sp.stats.rv_continuous):
    ...     def _rvs(self,  size=None, random_state=rng):
    ...         return rng.standard_normal(size) ** 2
    >>> X = NormalSquared()
    >>> Y = X()  # get a frozen version of the distribution
    >>> S = sp.sparse.random(3, 4, density=0.25, rng=rng, data_rvs=Y.rvs)
    """
    if n is None:
        n = m
    m, n = int(m), int(n)
    # make keyword syntax work for data_rvs e.g. data_rvs(size=7)
    if data_rvs is not None:
        def data_rvs_kw(size):
            return data_rvs(size)
    else:
        data_rvs_kw = None
    vals, ind = _random((m, n), density, format, dtype, rng, data_rvs_kw)
    return coo_matrix((vals, ind), shape=(m, n)).asformat(format)


def random(size):
    return rand(*size)


def random(size):
    return rand(*size)


def random(
    shape: tuple[int, int], seed: int = 2187, mask_fraction: float = 0.0,
) -> tuple[CoordinateArray, CoordinateArray, CoordinateArray | np.ma.MaskedArray[Any, Any]]:
    """Return random test data in the range 0 to 1.

    Args:
        shape (tuple(int, int)): 2D shape of data to return.
        seed (int, optional): Seed for random number generator, default 2187.
        mask_fraction (float, optional): Fraction of elements to mask, default 0.

    Return:
        Tuple of 3 arrays: ``x``, ``y``, ``z`` test data, ``z`` will be masked if
        ``mask_fraction`` is greater than zero.
    """
    ny, nx = shape
    x = np.arange(nx, dtype=np.float64)
    y = np.arange(ny, dtype=np.float64)
    x, y = np.meshgrid(x, y)

    rng = np.random.default_rng(seed)
    z = rng.uniform(size=shape)

    if mask_fraction > 0.0:
        mask_fraction = min(mask_fraction, 0.99)
        mask = rng.uniform(size=shape) < mask_fraction
        z = np.ma.array(z, mask=mask)  # type: ignore[no-untyped-call]

    return x, y, z

