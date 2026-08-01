
def test_hyper_as_trig():
    from sympy.simplify.fu import _osborne, _osbornei

    eq = sinh(x)**2 + cosh(x)**2
    t, f = hyper_as_trig(eq)
    assert f(fu(t)) == cosh(2*x)
    e, f = hyper_as_trig(tanh(x + y))
    assert f(TR12(e)) == (tanh(x) + tanh(y))/(tanh(x)*tanh(y) + 1)

    d = Dummy()
    assert _osborne(sinh(x), d) == I*sin(x*d)
    assert _osborne(tanh(x), d) == I*tan(x*d)
    assert _osborne(coth(x), d) == cot(x*d)/I
    assert _osborne(cosh(x), d) == cos(x*d)
    assert _osborne(sech(x), d) == sec(x*d)
    assert _osborne(csch(x), d) == csc(x*d)/I
    for func in (sinh, cosh, tanh, coth, sech, csch):
        h = func(pi)
        assert _osbornei(_osborne(h, d), d) == h
    # /!\ the _osborne functions are not meant to work
    # in the o(i(trig, d), d) direction so we just check
    # that they work as they are supposed to work
    assert _osbornei(cos(x*y + z), y) == cosh(x + z*I)
    assert _osbornei(sin(x*y + z), y) == sinh(x + z*I)/I
    assert _osbornei(tan(x*y + z), y) == tanh(x + z*I)/I
    assert _osbornei(cot(x*y + z), y) == coth(x + z*I)*I
    assert _osbornei(sec(x*y + z), y) == sech(x + z*I)
    assert _osbornei(csc(x*y + z), y) == csch(x + z*I)*I

