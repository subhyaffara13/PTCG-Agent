
def test_function_subs():
    S = Sum(x*f(y),(x,0,oo),(y,0,oo))
    assert S.subs(f(y),y) == Sum(x*y,(x,0,oo),(y,0,oo))
    assert S.subs(f(x),x) == S
    raises(ValueError, lambda: S.subs(f(y),x+y) )
    S = Sum(x*log(y),(x,0,oo),(y,0,oo))
    assert S.subs(log(y),y) == S
    S = Sum(x*f(y),(x,0,oo),(y,0,oo))
    assert S.subs(f(y),y) == Sum(x*y,(x,0,oo),(y,0,oo))

