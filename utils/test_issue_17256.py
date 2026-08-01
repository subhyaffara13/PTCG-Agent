
def test_issue_17256():
    from sympy.sets.fancysets import Range
    x = Symbol('x')
    s1 = Sum(x + 1, (x, 1, 9))
    s2 = Sum(x + 1, (x, Range(1, 10)))
    a = Symbol('a')
    r1 = s1.xreplace({x:a})
    r2 = s2.xreplace({x:a})

    assert r1.doit() == r2.doit()
    s1 = Sum(x + 1, (x, 0, 9))
    s2 = Sum(x + 1, (x, Range(10)))
    a = Symbol('a')
    r1 = s1.xreplace({x:a})
    r2 = s2.xreplace({x:a})
    assert r1 == r2

