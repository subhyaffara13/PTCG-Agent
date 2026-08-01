
def test_Dummy_force_dummy_index():
    raises(AssertionError, lambda: Dummy(dummy_index=1))
    assert Dummy('d', dummy_index=2) == Dummy('d', dummy_index=2)
    assert Dummy('d1', dummy_index=2) != Dummy('d2', dummy_index=2)
    d1 = Dummy('d', dummy_index=3)
    d2 = Dummy('d')
    # might fail if d1 were created with dummy_index >= 10**6
    assert d1 != d2
    d3 = Dummy('d', dummy_index=3)
    assert d1 == d3
    assert Dummy()._count == Dummy('d', dummy_index=3)._count

