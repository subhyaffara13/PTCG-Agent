
def test_issue_5654():
    a = Symbol('a')
    assert (1/(x**2+a**2)**2).nseries(x, x0=I*a, n=0) == \
        -I/(4*a**3*(-I*a + x)) - 1/(4*a**2*(-I*a + x)**2) + O(1, (x, I*a))
    assert (1/(x**2+a**2)**2).nseries(x, x0=I*a, n=1) == 3/(16*a**4) \
        -I/(4*a**3*(-I*a + x)) - 1/(4*a**2*(-I*a + x)**2) + O(-I*a + x, (x, I*a))


def test_issue_5654():
    assert residue(1/(x**2 + a**2)**2, x, a*I) == -I/(4*a**3)
    assert residue(1/s*1/(z - exp(s)), s, 0) == 1/(z - 1)
    assert residue((1 + k)/s*1/(z - exp(s)), s, 0) == k/(z - 1) + 1/(z - 1)

