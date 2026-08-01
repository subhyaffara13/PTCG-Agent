
def test_array_equivalent_compat():
    # see gh-13388
    m = np.array([(1, 2), (3, 4)], dtype=[("a", int), ("b", float)])
    n = np.array([(1, 2), (3, 4)], dtype=[("a", int), ("b", float)])
    assert array_equivalent(m, n, strict_nan=True)
    assert array_equivalent(m, n, strict_nan=False)

    m = np.array([(1, 2), (3, 4)], dtype=[("a", int), ("b", float)])
    n = np.array([(1, 2), (4, 3)], dtype=[("a", int), ("b", float)])
    assert not array_equivalent(m, n, strict_nan=True)
    assert not array_equivalent(m, n, strict_nan=False)

    m = np.array([(1, 2), (3, 4)], dtype=[("a", int), ("b", float)])
    n = np.array([(1, 2), (3, 4)], dtype=[("b", int), ("a", float)])
    assert not array_equivalent(m, n, strict_nan=True)
    assert not array_equivalent(m, n, strict_nan=False)

