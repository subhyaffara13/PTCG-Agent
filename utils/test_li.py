
def test_li():
    z = Symbol("z")
    zr = Symbol("z", real=True)
    zp = Symbol("z", positive=True)
    zn = Symbol("z", negative=True)

    assert li(0) is S.Zero
    assert li(1) is -oo
    assert li(oo) is oo

    assert isinstance(li(z), li)
    assert unchanged(li, -zp)
    assert unchanged(li, zn)

    assert diff(li(z), z) == 1/log(z)

    assert conjugate(li(z)) == li(conjugate(z))
    assert conjugate(li(-zr)) == li(-zr)
    assert unchanged(conjugate, li(-zp))
    assert unchanged(conjugate, li(zn))

    assert li(z).rewrite(Li) == Li(z) + li(2)
    assert li(z).rewrite(Ei) == Ei(log(z))
    assert li(z).rewrite(uppergamma) == (-log(1/log(z))/2 - log(-log(z)) +
                                         log(log(z))/2 - expint(1, -log(z)))
    assert li(z).rewrite(Si) == (-log(I*log(z)) - log(1/log(z))/2 +
                                 log(log(z))/2 + Ci(I*log(z)) + Shi(log(z)))
    assert li(z).rewrite(Ci) == (-log(I*log(z)) - log(1/log(z))/2 +
                                 log(log(z))/2 + Ci(I*log(z)) + Shi(log(z)))
    assert li(z).rewrite(Shi) == (-log(1/log(z))/2 + log(log(z))/2 +
                                  Chi(log(z)) - Shi(log(z)))
    assert li(z).rewrite(Chi) == (-log(1/log(z))/2 + log(log(z))/2 +
                                  Chi(log(z)) - Shi(log(z)))
    assert li(z).rewrite(hyper) ==(log(z)*hyper((1, 1), (2, 2), log(z)) -
                                   log(1/log(z))/2 + log(log(z))/2 + EulerGamma)
    assert li(z).rewrite(meijerg) == (-log(1/log(z))/2 - log(-log(z)) + log(log(z))/2 -
                                      meijerg(((), (1,)), ((0, 0), ()), -log(z)))

    assert gruntz(1/li(z), z, oo) is S.Zero
    assert li(z).series(z) == log(z)**5/600 + log(z)**4/96 + log(z)**3/18 + log(z)**2/4 + \
            log(z) + log(log(z)) + EulerGamma
    raises(ArgumentIndexError, lambda: li(z).fdiff(2))

