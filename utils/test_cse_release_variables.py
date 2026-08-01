
def test_cse_release_variables():
    from sympy.simplify.cse_main import cse_release_variables
    _0, _1, _2, _3, _4 = symbols('_:5')
    eqs = [(x + y - 1)**2, x,
        x + y, (x + y)/(2*x + 1) + (x + y - 1)**2,
        (2*x + 1)**(x + y)]
    r, e = cse(eqs, postprocess=cse_release_variables)
    # this can change in keeping with the intention of the function
    assert r, e == ([
    (x0, x + y), (x1, (x0 - 1)**2), (x2, 2*x + 1),
    (_3, x0/x2 + x1), (_4, x2**x0), (x2, None), (_0, x1),
    (x1, None), (_2, x0), (x0, None), (_1, x)], (_0, _1, _2, _3, _4))
    r.reverse()
    r = [(s, v) for s, v in r if v is not None]
    assert eqs == [i.subs(r) for i in e]

