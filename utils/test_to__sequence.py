
def test_to_Sequence():
    x = symbols('x')
    R, Dx = DifferentialOperators(ZZ.old_poly_ring(x), 'Dx')
    n = symbols('n', integer=True)
    _, Sn = RecurrenceOperators(ZZ.old_poly_ring(n), 'Sn')
    p = HolonomicFunction(x**2*Dx**4 + x + Dx, x).to_sequence()
    q = [(HolonomicSequence(1 + (n + 2)*Sn**2 + (n**4 + 6*n**3 + 11*n**2 + 6*n)*Sn**3), 0, 1)]
    assert p == q
    p = HolonomicFunction(x**2*Dx**4 + x**3 + Dx**2, x).to_sequence()
    q = [(HolonomicSequence(1 + (n**4 + 14*n**3 + 72*n**2 + 163*n + 140)*Sn**5), 0, 0)]
    assert p == q
    p = HolonomicFunction(x**3*Dx**4 + 1 + Dx**2, x).to_sequence()
    q = [(HolonomicSequence(1 + (n**4 - 2*n**3 - n**2 + 2*n)*Sn + (n**2 + 3*n + 2)*Sn**2), 0, 0)]
    assert p == q
    p = HolonomicFunction(3*x**3*Dx**4 + 2*x*Dx + x*Dx**3, x).to_sequence()
    q = [(HolonomicSequence(2*n + (3*n**4 - 6*n**3 - 3*n**2 + 6*n)*Sn + (n**3 + 3*n**2 + 2*n)*Sn**2), 0, 1)]
    assert p == q

