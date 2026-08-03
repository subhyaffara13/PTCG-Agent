import itertools

def test_memoverlap_accumulate_cmp(ufunc, dtype):
    if ufunc.signature:
        pytest.skip('For generic signatures only')
    for size in (2, 8, 32, 64, 128, 256):
        arr = np.array([0, 1, 1] * size, dtype=dtype)
        acc = ufunc.accumulate(arr, dtype='?')
        acc_u8 = acc.view(np.uint8)
        exp = np.array(list(itertools.accumulate(arr, ufunc)), dtype=np.uint8)
        assert_equal(exp, acc_u8)

