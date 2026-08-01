
def test_swapped_byte_order_real(func):
    rng = np.random.RandomState(1234)
    x = rng.rand(10)
    assert_allclose(func(swap_byteorder(x)), func(x))

