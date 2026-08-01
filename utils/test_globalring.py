
def test_globalring():
    Qxy = QQ.old_frac_field(x, y)
    R = QQ.old_poly_ring(x, y)
    X = R.convert(x)
    Y = R.convert(y)

    assert x in R
    assert 1/x not in R
    assert 1/(1 + x) not in R
    assert Y in R
    assert X * (Y**2 + 1) == R.convert(x * (y**2 + 1))
    assert X + 1 == R.convert(x + 1)
    raises(ExactQuotientFailed, lambda: X/Y)
    raises(TypeError, lambda: x/Y)
    raises(TypeError, lambda: X/y)
    assert X**2 / X == X

    assert R.from_GlobalPolynomialRing(ZZ.old_poly_ring(x, y).convert(x), ZZ.old_poly_ring(x, y)) == X
    assert R.from_FractionField(Qxy.convert(x), Qxy) == X
    assert R.from_FractionField(Qxy.convert(x/y), Qxy) is None

    assert R._sdm_to_vector(R._vector_to_sdm([X, Y], R.order), 2) == [X, Y]

