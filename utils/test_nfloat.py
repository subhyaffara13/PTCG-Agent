from typing import Dict, Tuple

def test_nfloat():
    from sympy.core.basic import _aresame
    from sympy.polys.rootoftools import rootof

    x = Symbol("x")
    eq = x**Rational(4, 3) + 4*x**(S.One/3)/3
    assert _aresame(nfloat(eq), x**Rational(4, 3) + (4.0/3)*x**(S.One/3))
    assert _aresame(nfloat(eq, exponent=True), x**(4.0/3) + (4.0/3)*x**(1.0/3))
    eq = x**Rational(4, 3) + 4*x**(x/3)/3
    assert _aresame(nfloat(eq), x**Rational(4, 3) + (4.0/3)*x**(x/3))
    big = 12345678901234567890
    # specify precision to match value used in nfloat
    Float_big = Float(big, 15)
    assert _aresame(nfloat(big), Float_big)
    assert _aresame(nfloat(big*x), Float_big*x)
    assert _aresame(nfloat(x**big, exponent=True), x**Float_big)
    assert nfloat(cos(x + sqrt(2))) == cos(x + nfloat(sqrt(2)))

    # issue 6342
    f = S('x*lamda + lamda**3*(x/2 + 1/2) + lamda**2 + 1/4')
    assert not any(a.free_symbols for a in solveset(f.subs(x, -0.139)))

    # issue 6632
    assert nfloat(-100000*sqrt(2500000001) + 5000000001) == \
        9.99999999800000e-11

    # issue 7122
    eq = cos(3*x**4 + y)*rootof(x**5 + 3*x**3 + 1, 0)
    assert str(nfloat(eq, exponent=False, n=1)) == '-0.7*cos(3.0*x**4 + y)'

    # issue 10933
    for ti in (dict, Dict):
        d = ti({S.Half: S.Half})
        n = nfloat(d)
        assert isinstance(n, ti)
        assert _aresame(list(n.items()).pop(), (S.Half, Float(.5)))
    for ti in (dict, Dict):
        d = ti({S.Half: S.Half})
        n = nfloat(d, dkeys=True)
        assert isinstance(n, ti)
        assert _aresame(list(n.items()).pop(), (Float(.5), Float(.5)))
    d = [S.Half]
    n = nfloat(d)
    assert type(n) is list
    assert _aresame(n[0], Float(.5))
    assert _aresame(nfloat(Eq(x, S.Half)).rhs, Float(.5))
    assert _aresame(nfloat(S(True)), S(True))
    assert _aresame(nfloat(Tuple(S.Half))[0], Float(.5))
    assert nfloat(Eq((3 - I)**2/2 + I, 0)) == S.false
    # pass along kwargs
    assert nfloat([{S.Half: x}], dkeys=True) == [{Float(0.5): x}]

    # Issue 17706
    A = MutableMatrix([[1, 2], [3, 4]])
    B = MutableMatrix(
        [[Float('1.0', precision=53), Float('2.0', precision=53)],
        [Float('3.0', precision=53), Float('4.0', precision=53)]])
    assert _aresame(nfloat(A), B)
    A = ImmutableMatrix([[1, 2], [3, 4]])
    B = ImmutableMatrix(
        [[Float('1.0', precision=53), Float('2.0', precision=53)],
        [Float('3.0', precision=53), Float('4.0', precision=53)]])
    assert _aresame(nfloat(A), B)

    # issue 22524
    f = Function('f')
    assert not nfloat(f(2)).atoms(Float)

