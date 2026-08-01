
def test_array_collapse():
    assert not isinstance(m.vectorized_func(1, 2, 3), np.ndarray)
    assert not isinstance(m.vectorized_func(np.array(1), 2, 3), np.ndarray)
    z = m.vectorized_func([1], 2, 3)
    assert isinstance(z, np.ndarray)
    assert z.shape == (1,)
    z = m.vectorized_func(1, [[[2]]], 3)
    assert isinstance(z, np.ndarray)
    assert z.shape == (1, 1, 1)

