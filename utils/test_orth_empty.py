
def test_orth_empty(dt):
    a = np.empty((0, 0), dtype=dt)
    a0 = np.eye(2, dtype=dt)

    oa = orth(a)
    assert oa.dtype == orth(a0).dtype
    assert oa.shape == (0, 0)

