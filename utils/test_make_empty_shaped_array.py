
def test_make_empty_shaped_array():
    m.make_empty_shaped_array()

    # empty shape means numpy scalar, PEP 3118
    assert m.scalar_int().ndim == 0
    assert m.scalar_int().shape == ()
    assert m.scalar_int() == 42

