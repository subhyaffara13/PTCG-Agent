
def test_SeqFormula():
    s = SeqFormula(n**2, (n, 0, 5))

    assert isinstance(s, SeqFormula)
    assert s.formula == n**2
    assert s.coeff(3) == 9

    assert list(s) == [i**2 for i in range(6)]
    assert s[:] == [i**2 for i in range(6)]
    assert SeqFormula(n**2, (n, -oo, 0))[0:6] == [i**2 for i in range(6)]

    assert SeqFormula(n**2, (0, oo)) == SeqFormula(n**2, (n, 0, oo))

    assert SeqFormula(n**2, (0, m)).subs(m, x) == SeqFormula(n**2, (0, x))
    assert SeqFormula(m*n**2, (n, 0, oo)).subs(m, x) == \
        SeqFormula(x*n**2, (n, 0, oo))

    raises(ValueError, lambda: SeqFormula(n**2, (0, 1, 2)))
    raises(ValueError, lambda: SeqFormula(n**2, (n, -oo, oo)))
    raises(ValueError, lambda: SeqFormula(m*n**2, (0, oo)))

    seq = SeqFormula(x*(y**2 + z), (z, 1, 100))
    assert seq.expand() == SeqFormula(x*y**2 + x*z, (z, 1, 100))
    seq = SeqFormula(sin(x*(y**2 + z)),(z, 1, 100))
    assert seq.expand(trig=True) == SeqFormula(sin(x*y**2)*cos(x*z) + sin(x*z)*cos(x*y**2), (z, 1, 100))
    assert seq.expand() == SeqFormula(sin(x*y**2 + x*z), (z, 1, 100))
    assert seq.expand(trig=False) == SeqFormula(sin(x*y**2 + x*z), (z, 1, 100))
    seq = SeqFormula(exp(x*(y**2 + z)), (z, 1, 100))
    assert seq.expand() == SeqFormula(exp(x*y**2)*exp(x*z), (z, 1, 100))
    assert seq.expand(power_exp=False) == SeqFormula(exp(x*y**2 + x*z), (z, 1, 100))
    assert seq.expand(mul=False, power_exp=False) == SeqFormula(exp(x*(y**2 + z)), (z, 1, 100))

