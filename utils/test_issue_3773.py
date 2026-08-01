
def test_issue_3773():
    x = symbols('x')
    z, phi, r = symbols('z phi r')
    c, A, B, N = symbols('c A B N', cls=Wild)
    l = Wild('l', exclude=(0,))

    eq = z * sin(2*phi) * r**7
    matcher = c * sin(phi*N)**l * r**A * log(r)**B

    assert eq.match(matcher) == {c: z, l: 1, N: 2, A: 7, B: 0}
    assert (-eq).match(matcher) == {c: -z, l: 1, N: 2, A: 7, B: 0}
    assert (x*eq).match(matcher) == {c: x*z, l: 1, N: 2, A: 7, B: 0}
    assert (-7*x*eq).match(matcher) == {c: -7*x*z, l: 1, N: 2, A: 7, B: 0}

    matcher = c*sin(phi*N)**l * r**A

    assert eq.match(matcher) == {c: z, l: 1, N: 2, A: 7}
    assert (-eq).match(matcher) == {c: -z, l: 1, N: 2, A: 7}
    assert (x*eq).match(matcher) == {c: x*z, l: 1, N: 2, A: 7}
    assert (-7*x*eq).match(matcher) == {c: -7*x*z, l: 1, N: 2, A: 7}

