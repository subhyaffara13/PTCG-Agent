
def test_macaulay_resultant_init():
    """Test init method of MacaulayResultant."""

    assert macaulay.polynomials == [p, q]
    assert macaulay.variables == [x, y]
    assert macaulay.n == 2
    assert macaulay.degrees == [1, 1]
    assert macaulay.degree_m == 1
    assert macaulay.monomials_size == 2

