
def test_DifferentialExtension_printing():
    DE = DifferentialExtension(exp(2*x**2) + log(exp(x**2) + 1), x)
    assert repr(DE) == ("DifferentialExtension(dict([('f', exp(2*x**2) + log(exp(x**2) + 1)), "
        "('x', x), ('T', [x, t0, t1]), ('D', [Poly(1, x, domain='ZZ'), Poly(2*x*t0, t0, domain='ZZ[x]'), "
        "Poly(2*t0*x/(t0 + 1), t1, domain='ZZ(x,t0)')]), ('fa', Poly(t1 + t0**2, t1, domain='ZZ[t0]')), "
        "('fd', Poly(1, t1, domain='ZZ')), ('Tfuncs', [Lambda(i, exp(i**2)), Lambda(i, log(t0 + 1))]), "
        "('backsubs', []), ('exts', [None, 'exp', 'log']), ('extargs', [None, x**2, t0 + 1]), "
        "('cases', ['base', 'exp', 'primitive']), ('case', 'primitive'), ('t', t1), "
        "('d', Poly(2*t0*x/(t0 + 1), t1, domain='ZZ(x,t0)')), ('newf', t0**2 + t1), ('level', -1), "
        "('dummy', False)]))")

    assert str(DE) == ("DifferentialExtension({fa=Poly(t1 + t0**2, t1, domain='ZZ[t0]'), "
        "fd=Poly(1, t1, domain='ZZ'), D=[Poly(1, x, domain='ZZ'), Poly(2*x*t0, t0, domain='ZZ[x]'), "
        "Poly(2*t0*x/(t0 + 1), t1, domain='ZZ(x,t0)')]})")

