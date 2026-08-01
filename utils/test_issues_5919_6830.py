
def test_issues_5919_6830():
    # issue 5919
    n = -1 + 1/x
    z = n/x/(-n)**2 - 1/n/x
    assert expand(z) == 1/(x**2 - 2*x + 1) - 1/(x - 2 + 1/x) - 1/(-x + 1)

    # issue 6830
    p = (1 + x)**2
    assert expand_multinomial((1 + x*p)**2) == (
        x**2*(x**4 + 4*x**3 + 6*x**2 + 4*x + 1) + 2*x*(x**2 + 2*x + 1) + 1)
    assert expand_multinomial((1 + (y + x)*p)**2) == (
        2*((x + y)*(x**2 + 2*x + 1)) + (x**2 + 2*x*y + y**2)*
        (x**4 + 4*x**3 + 6*x**2 + 4*x + 1) + 1)
    A = Symbol('A', commutative=False)
    p = (1 + A)**2
    assert expand_multinomial((1 + x*p)**2) == (
        x**2*(1 + 4*A + 6*A**2 + 4*A**3 + A**4) + 2*x*(1 + 2*A + A**2) + 1)
    assert expand_multinomial((1 + (y + x)*p)**2) == (
        (x + y)*(1 + 2*A + A**2)*2 + (x**2 + 2*x*y + y**2)*
        (1 + 4*A + 6*A**2 + 4*A**3 + A**4) + 1)
    assert expand_multinomial((1 + (y + x)*p)**3) == (
        (x + y)*(1 + 2*A + A**2)*3 + (x**2 + 2*x*y + y**2)*(1 + 4*A +
        6*A**2 + 4*A**3 + A**4)*3 + (x**3 + 3*x**2*y + 3*x*y**2 + y**3)*(1 + 6*A
        + 15*A**2 + 20*A**3 + 15*A**4 + 6*A**5 + A**6) + 1)
    # unevaluate powers
    eq = (Pow((x + 1)*((A + 1)**2), 2, evaluate=False))
    # - in this case the base is not an Add so no further
    #   expansion is done
    assert expand_multinomial(eq) == \
        (x**2 + 2*x + 1)*(1 + 4*A + 6*A**2 + 4*A**3 + A**4)
    # - but here, the expanded base *is* an Add so it gets expanded
    eq = (Pow(((A + 1)**2), 2, evaluate=False))
    assert expand_multinomial(eq) == 1 + 4*A + 6*A**2 + 4*A**3 + A**4

    # coverage
    def ok(a, b, n):
        e = (a + I*b)**n
        return verify_numerically(e, expand_multinomial(e))

    for a in [2, S.Half]:
        for b in [3, R(1, 3)]:
            for n in range(2, 6):
                assert ok(a, b, n)

    assert expand_multinomial((x + 1 + O(z))**2) == \
        1 + 2*x + x**2 + O(z)
    assert expand_multinomial((x + 1 + O(z))**3) == \
        1 + 3*x + 3*x**2 + x**3 + O(z)

    assert expand_multinomial(3**(x + y + 3)) == 27*3**(x + y)

