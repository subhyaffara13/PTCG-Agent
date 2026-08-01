
def test_inversion_exp_real_nonreal_shift():
    from sympy.core.symbol import Symbol
    from sympy.functions.special.delta_functions import DiracDelta
    r = Symbol('r', real=True)
    c = Symbol('c', extended_real=False)
    a = 1 + 2*I
    z = Symbol('z')
    assert not meijerint_inversion(exp(r*s), s, t).is_Piecewise
    assert meijerint_inversion(exp(a*s), s, t) is None
    assert meijerint_inversion(exp(c*s), s, t) is None
    f = meijerint_inversion(exp(z*s), s, t)
    assert f.is_Piecewise
    assert isinstance(f.args[0][0], DiracDelta)

