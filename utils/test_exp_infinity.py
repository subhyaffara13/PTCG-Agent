
def test_exp_infinity():
    assert exp(I*y) != nan
    assert refine(exp(I*oo)) is nan
    assert refine(exp(-I*oo)) is nan
    assert exp(y*I*oo) != nan
    assert exp(zoo) is nan
    x = Symbol('x', extended_real=True, finite=False)
    assert exp(x).is_complex is None

