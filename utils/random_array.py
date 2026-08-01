
def random_array(shape, *, density=0.01, format='coo', dtype=None,
                 rng=None, data_sampler=None):
    """Return a sparse array of uniformly random numbers in [0, 1).

    Returns a sparse array with the given shape and density
    where values are generated uniformly randomly in the range [0, 1).

    Parameters
    ----------
    shape : tuple of int
        shape of the array.
    density : real, optional (default: 0.01)
        density of the generated matrix: density equal to one means a full
        matrix, density of 0 means a matrix with no non-zero items.
    format : str, optional (default: 'coo')
        sparse matrix format.
    dtype : dtype, optional (default: np.float64)
        type of the returned matrix values.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

        This random state will be used for sampling ``indices`` (the sparsity
        structure), and by default for the data values too (see `data_sampler`).
    data_sampler : callable, optional (default depends on dtype)
        Sampler of random data values with keyword arg ``size``.
        This function should take a single keyword argument ``size`` specifying
        the length of its returned ndarray. It is used to generate the nonzero
        values in the matrix after the locations of those values are chosen.
        By default, uniform [0, 1) random values are used unless `dtype` is
        an integer (default uniform integers from that dtype) or
        complex (default uniform over the unit square in the complex plane).
        For these, the `rng` is used e.g. ``rng.uniform(size=size)``.

    Returns
    -------
    res : sparse array
        Random sparse array.

    Examples
    --------

    Passing a ``np.random.Generator`` instance for better performance:

    >>> import numpy as np
    >>> import scipy as sp
    >>> rng = np.random.default_rng()

    Default sampling uniformly from [0, 1):

    >>> S = sp.sparse.random_array((3, 4), density=0.25, rng=rng)

    Providing a sampler for the values:

    >>> rvs = sp.stats.poisson(25, loc=10).rvs
    >>> S = sp.sparse.random_array((3, 4), density=0.25,
    ...                            rng=rng, data_sampler=rvs)
    >>> S.toarray()
    array([[ 36.,   0.,  33.,   0.],   # random
           [  0.,   0.,   0.,   0.],
           [  0.,   0.,  36.,   0.]])

    Providing a sampler for uint values:

    >>> def random_uint32_to_100(size=None):
    ...     return rng.integers(100, size=size, dtype=np.uint32)
    >>> S = sp.sparse.random_array((3, 4), density=0.25, rng=rng,
    ...                            data_sampler=random_uint32_to_100)

    Building a custom distribution.
    This example builds a squared normal from np.random:

    >>> def np_normal_squared(size=None, rng=rng):
    ...     return rng.standard_normal(size) ** 2
    >>> S = sp.sparse.random_array((3, 4), density=0.25, rng=rng,
    ...                            data_sampler=np_normal_squared)

    Or we can build it from sp.stats style rvs functions:

    >>> def sp_stats_normal_squared(size=None, rng=rng):
    ...     std_normal = sp.stats.distributions.norm_gen().rvs
    ...     return std_normal(size=size, random_state=rng) ** 2
    >>> S = sp.sparse.random_array((3, 4), density=0.25, rng=rng,
    ...                            data_sampler=sp_stats_normal_squared)

    Or we can subclass sp.stats rv_continuous or rv_discrete:

    >>> class NormalSquared(sp.stats.rv_continuous):
    ...     def _rvs(self,  size=None, random_state=rng):
    ...         return rng.standard_normal(size) ** 2
    >>> X = NormalSquared()
    >>> Y = X().rvs
    >>> S = sp.sparse.random_array((3, 4), density=0.25,
    ...                            rng=rng, data_sampler=Y)
    """
    data, ind = _random(shape, density, format, dtype, rng, data_sampler)

    # downcast, if safe, before calling coo_constructor
    idx_dtype = get_index_dtype(maxval=max(shape))
    ind = tuple(np.asarray(co, dtype=idx_dtype) for co in ind)
    return coo_array((data, ind), shape=shape).asformat(format)

