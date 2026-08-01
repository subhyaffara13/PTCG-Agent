
def test_issue_21022():
    from sympy.core.sympify import sympify

    eqs = [
    'k-16',
    'p-8',
    'y*y+z*z-x*x',
    'd - x + p',
    'd*d+k*k-y*y',
    'z*z-p*p-k*k',
    'abc-efg',
    ]
    efg = Symbol('efg')
    eqs = [sympify(x) for x in eqs]

    syb = list(ordered(set.union(*[x.free_symbols for x in eqs])))
    res = nonlinsolve(eqs, syb)

    ans = FiniteSet(
    (efg, 32, efg, 16, 8, 40, -16*sqrt(5), -8*sqrt(5)),
    (efg, 32, efg, 16, 8, 40, -16*sqrt(5), 8*sqrt(5)),
    (efg, 32, efg, 16, 8, 40, 16*sqrt(5), -8*sqrt(5)),
    (efg, 32, efg, 16, 8, 40, 16*sqrt(5), 8*sqrt(5)),
    )
    assert len(res) == len(ans) == 4
    assert res == ans
    for result in res.args:
        assert len(result) == 8

