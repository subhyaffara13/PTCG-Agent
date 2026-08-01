
def test__broadcast_concatenate(xp):
    # test that _broadcast_concatenate properly broadcasts arrays along all
    # axes except `axis`, then concatenates along axis
    rng = np.random.default_rng(7544340069)
    a = rng.random((5, 4, 4, 3, 1, 6))
    b = rng.random((4, 1, 8, 2, 6))
    arrays = (xp.asarray(a), xp.asarray(b))
    c = stats._axis_nan_policy._broadcast_concatenate(arrays, axis=-3, xp=xp)
    # broadcast manually as an independent check
    a = np.tile(a, (1, 1, 1, 1, 2, 1))
    b = np.tile(b[None, ...], (5, 1, 4, 1, 1, 1))
    for index in product(*(range(i) for i in c.shape)):
        i, j, k, l, m, n = index
        if l < a.shape[-3]:
            assert a[i, j, k, l, m, n] == c[i, j, k, l, m, n]
        else:
            assert b[i, j, k, l - a.shape[-3], m, n] == c[i, j, k, l, m, n]

