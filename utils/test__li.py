
def test_Li():
    assert Li(2) is S.Zero
    assert Li(oo) is oo

    assert isinstance(Li(z), Li)

    assert diff(Li(z), z) == 1/log(z)

    assert gruntz(1/Li(z), z, oo) is S.Zero
    assert Li(z).rewrite(li) == li(z) - li(2)
    assert Li(z).series(z) == \
        log(z)**5/600 + log(z)**4/96 + log(z)**3/18 + log(z)**2/4 + log(z) + log(log(z)) - li(2) + EulerGamma
    raises(ArgumentIndexError, lambda: Li(z).fdiff(2))

