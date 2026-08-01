
def test_swapped_byte_order(func):
    rng = np.random.RandomState(1234)
    x = rng.rand(10)
    swapped_dt = x.dtype.newbyteorder('S')
    assert_allclose(func(x.astype(swapped_dt)), func(x))

