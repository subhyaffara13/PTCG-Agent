
def test_nep50_weak_integers(dtype):
    # Avoids warning (different code path for scalars)
    scalar_type = np.dtype(dtype).type

    maxint = int(np.iinfo(dtype).max)

    with np.errstate(over="warn"):
        with pytest.warns(RuntimeWarning):
            res = scalar_type(100) + maxint
    assert res.dtype == dtype

    # Array operations are not expected to warn, but should give the same
    # result dtype.
    res = np.array(100, dtype=dtype) + maxint
    assert res.dtype == dtype

