
def test_issue_11230():
    # a specific test that always failed
    a, b, f, k, l, i = symbols('a b f k l i')
    p = [a*b*f*k*l, a*i*k**2*l, f*i*k**2*l]
    R, C = cse(p)
    assert not any(i.is_Mul for a in C for i in a.args)

    # random tests for the issue
    from sympy.core.random import choice
    from sympy.core.function import expand_mul
    s = symbols('a:m')
    # 35 Mul tests, none of which should ever fail
    ex = [Mul(*[choice(s) for i in range(5)]) for i in range(7)]
    for p in subsets(ex, 3):
        p = list(p)
        R, C = cse(p)
        assert not any(i.is_Mul for a in C for i in a.args)
        for ri in reversed(R):
            for i in range(len(C)):
                C[i] = C[i].subs(*ri)
        assert p == C
    # 35 Add tests, none of which should ever fail
    ex = [Add(*[choice(s[:7]) for i in range(5)]) for i in range(7)]
    for p in subsets(ex, 3):
        p = list(p)
        R, C = cse(p)
        assert not any(i.is_Add for a in C for i in a.args)
        for ri in reversed(R):
            for i in range(len(C)):
                C[i] = C[i].subs(*ri)
        # use expand_mul to handle cases like this:
        # p = [a + 2*b + 2*e, 2*b + c + 2*e, b + 2*c + 2*g]
        # x0 = 2*(b + e) is identified giving a rebuilt p that
        # is now `[a + 2*(b + e), c + 2*(b + e), b + 2*c + 2*g]`
        assert p == [expand_mul(i) for i in C]

