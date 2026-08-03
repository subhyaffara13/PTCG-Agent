import math


def _random(shape, density=0.01, format=None, dtype=None,
            rng=None, data_sampler=None):
    if density < 0 or density > 1:
        raise ValueError("density expected to be 0 <= density <= 1")

    tot_prod = math.prod(shape)  # use `math` for when prod is >= 2**64

    # Number of non zero values
    size = int(round(density * tot_prod))

    rng = check_random_state(rng)

    if data_sampler is None:
        if np.issubdtype(dtype, np.integer):
            def data_sampler(size):
                return rng_integers(rng,
                                    np.iinfo(dtype).min,
                                    np.iinfo(dtype).max,
                                    size,
                                    dtype=dtype)
        elif np.issubdtype(dtype, np.complexfloating):
            def data_sampler(size):
                return (rng.uniform(size=size) +
                        rng.uniform(size=size) * 1j)
        else:
            data_sampler = rng.uniform

    idx_dtype = get_index_dtype(maxval=max(shape))
    # rng.choice uses int64 if first arg is an int
    if tot_prod <= np.iinfo(np.int64).max:
        raveled_ind = rng.choice(tot_prod, size=size, replace=False)
        ind = np.unravel_index(raveled_ind, shape=shape, order='F')
        ind = tuple(np.asarray(co, idx_dtype) for co in ind)
    else:
        # for ravel indices bigger than dtype max, use sets to remove duplicates
        ndim = len(shape)
        seen = set()
        while len(seen) < size:
            dsize = size - len(seen)
            seen.update(map(tuple, rng_integers(rng, shape, size=(dsize, ndim))))
        ind = tuple(np.array(list(seen), dtype=idx_dtype).T)

    # size kwarg allows eg data_sampler=partial(np.random.poisson, lam=5)
    vals = data_sampler(size=size).astype(dtype, copy=False)
    return vals, ind

