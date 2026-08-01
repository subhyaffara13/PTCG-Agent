
def test_scalar_repr_special(scalar, legacy_repr, representation):
    # Test NEP 51 scalar repr (and legacy option) for numeric types
    assert repr(scalar) == representation

    with np.printoptions(legacy="1.25"):
        assert repr(scalar) == legacy_repr

