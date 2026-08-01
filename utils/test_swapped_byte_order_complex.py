
def test_swapped_byte_order_complex(func):
    rng = np.random.RandomState(1234)
    x = rng.rand(10) + 1j * rng.rand(10)
    assert_allclose(func(swap_byteorder(x)), func(x))

