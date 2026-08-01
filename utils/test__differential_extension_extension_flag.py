
def test_DifferentialExtension_extension_flag():
    raises(ValueError, lambda: DifferentialExtension(extension={'T': [x, t]}))
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)]})
    assert DE._important_attrs == (None, None, [Poly(1, x), Poly(t, t)], [x, t],
        None, None, None, None)
    assert DE.d == Poly(t, t)
    assert DE.t == t
    assert DE.level == -1
    assert DE.cases == ['base', 'exp']
    assert DE.x == x
    assert DE.case == 'exp'

    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)],
        'exts': [None, 'exp'], 'extargs': [None, x]})
    assert DE._important_attrs == (None, None, [Poly(1, x), Poly(t, t)], [x, t],
        None, None, [None, 'exp'], [None, x])
    raises(ValueError, lambda: DifferentialExtension())

