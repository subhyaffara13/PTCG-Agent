
def test_HolonomicFunction_power():
    x = symbols('x')
    R, Dx = DifferentialOperators(ZZ.old_poly_ring(x), 'Dx')
    p = HolonomicFunction(Dx+x+x*Dx**2, x)
    a = HolonomicFunction(Dx, x)
    for n in range(10):
        assert a == p**n
        a *= p

