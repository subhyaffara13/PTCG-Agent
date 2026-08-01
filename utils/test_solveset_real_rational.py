
def test_solveset_real_rational():
    """Test solveset_real for rational functions"""
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    assert solveset_real((x - y**3) / ((y**2)*sqrt(1 - y**2)), x) \
        == FiniteSet(y**3)
    # issue 4486
    assert solveset_real(2*x/(x + 2) - 1, x) == FiniteSet(2)

