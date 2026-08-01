
def test_memoverlap_accumulate_symmetric(ufunc, dtype):
    if ufunc.signature:
        pytest.skip('For generic signatures only')
    with np.errstate(all='ignore'):
        for size in (2, 8, 32, 64, 128, 256):
            arr = np.array([0, 1, 2] * size).astype(dtype)
            acc = ufunc.accumulate(arr, dtype=dtype)
            exp = np.array(list(itertools.accumulate(arr, ufunc)), dtype=dtype)
            assert_equal(exp, acc)

