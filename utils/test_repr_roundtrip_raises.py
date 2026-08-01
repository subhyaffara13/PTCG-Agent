
def test_repr_roundtrip_raises():
    mi = MultiIndex.from_product([list("ab"), range(3)], names=["first", "second"])
    msg = "Must pass both levels and codes"
    with pytest.raises(TypeError, match=msg):
        eval(repr(mi))

