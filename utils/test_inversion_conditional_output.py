
def test_inversion_conditional_output():
    from sympy.core.symbol import Symbol
    from sympy.integrals.transforms import InverseLaplaceTransform

    a = Symbol('a', positive=True)
    F = sqrt(pi/a)*exp(-2*sqrt(a)*sqrt(s))
    f = meijerint_inversion(F, s, t)
    assert not f.is_Piecewise

    b = Symbol('b', real=True)
    F = F.subs(a, b)
    f2 = meijerint_inversion(F, s, t)
    assert f2.is_Piecewise
    # first piece is same as f
    assert f2.args[0][0] == f.subs(a, b)
    # last piece is an unevaluated transform
    assert f2.args[-1][1]
    ILT = InverseLaplaceTransform(F, s, t, None)
    assert f2.args[-1][0] == ILT or f2.args[-1][0] == ILT.as_integral

