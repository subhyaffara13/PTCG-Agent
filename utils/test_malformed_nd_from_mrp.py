
def test_malformed_nd_from_mrp(xp, ndim: int):
    shape = (1,) * (ndim - 1) + (2,)
    with pytest.raises(ValueError, match='Expected `mrp` to have shape'):
        Rotation.from_mrp(xp.ones(shape))

