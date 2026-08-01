
def get_arrays(n_arrays, *, dtype=np.float64, xp=np, shape=(30,), device=None,
               seed=84912165484321):
    rng = np.random.default_rng(seed)

    datas = []
    for i in range(n_arrays):
        data = 10*rng.random(size=shape)
        if xp.isdtype(dtype, 'complex floating'):
            data = data * 10j*rng.standard_normal(size=shape)
        data = xp.asarray(data, dtype=dtype, device=device)
        datas.append(data)

    return datas


def get_arrays(n_arrays, *, dtype='float64', xp=np, shape=(7, 8), all_unique=True,
               seed=84912165484321):
    mxp = marray._get_namespace(xp)
    rng = np.random.default_rng(seed)

    datas, masks = [], []
    for i in range(n_arrays):
        data = (rng.random(size=shape) if all_unique
                else rng.integers(np.min(shape) // 2, size=shape))
        if dtype.startswith('complex'):
            data = 10*data * 10j*rng.standard_normal(size=shape)
        data = data.astype(dtype)
        datas.append(data)
        mask = rng.random(size=shape) > 0.75
        masks.append(mask)

    marrays = []
    nan_arrays = []
    for array, mask in zip(datas, masks):
        marrays.append(mxp.asarray(array, mask=mask))
        nan_array = array.copy()
        nan_array[mask] = xp.nan
        nan_arrays.append(nan_array)

    return mxp, marrays, nan_arrays

