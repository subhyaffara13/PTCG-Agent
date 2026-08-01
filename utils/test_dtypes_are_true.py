
def test_dtypes_are_true():
    # test for gh-6294
    assert bool(np.dtype('f8'))
    assert bool(np.dtype('i8'))
    assert bool(np.dtype([('a', 'i8'), ('b', 'f4')]))

