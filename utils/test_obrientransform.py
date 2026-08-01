
def test_obrientransform(dtype, n_arrays, xp):
    # obrientransform is not yet vectorized
    mxp, marrays, narrays = get_arrays(n_arrays, dtype=dtype, shape=(25,), xp=xp)
    res = stats.obrientransform(*marrays)
    ref = stats.obrientransform(*narrays, nan_policy='omit')
    for res_i, ref_i in zip(res, ref):
        xp_assert_close(res_i.data[~res_i.mask],
                        xp.asarray(ref_i[~np.isnan(ref_i)], dtype=getattr(xp, dtype)))

