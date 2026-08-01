
def test_ComplexRegion_FiniteSet():
    x, y, z, a, b, c = symbols('x y z a b c')

    # Issue #9669
    assert ComplexRegion(FiniteSet(a, b, c)*FiniteSet(x, y, z)) == \
        FiniteSet(a + I*x, a + I*y, a + I*z, b + I*x, b + I*y,
                  b + I*z, c + I*x, c + I*y, c + I*z)
    assert ComplexRegion(FiniteSet(2)*FiniteSet(3)) == FiniteSet(2 + 3*I)

