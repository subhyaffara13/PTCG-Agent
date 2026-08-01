
def test_undef_fcn_float_issue_6938():
    f = Function('ceil')
    assert not f(0.3).is_number
    f = Function('sin')
    assert not f(0.3).is_number
    assert not f(pi).evalf().is_number
    x = Symbol('x')
    assert not f(x).evalf(subs={x:1.2}).is_number

