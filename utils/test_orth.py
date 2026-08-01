
def test_orth():
    dtypes = [np.float32, np.float64, np.complex64, np.complex128]
    sizes = [1, 2, 3, 10, 100]
    for dt, n in itertools.product(dtypes, sizes):
        _check_orth(n, dt)

