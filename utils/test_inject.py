
def test_inject():
    assert ZZ.inject(x, y, z) == ZZ[x, y, z]
    assert ZZ[x].inject(y, z) == ZZ[x, y, z]
    assert ZZ.frac_field(x).inject(y, z) == ZZ.frac_field(x, y, z)
    raises(GeneratorsError, lambda: ZZ[x].inject(x))

