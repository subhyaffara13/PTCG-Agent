
def test_SymPy_substitution_functions():
    # subs
    ss1 = StateSpace(Matrix([s]), Matrix([(s + 1)**2]), Matrix([s**2 - 1]), Matrix([2*s]))
    ss2 = StateSpace(Matrix([s + p]), Matrix([(s + 1)*(p - 1)]), Matrix([p**3 - s**3]), Matrix([s - p]))

    assert ss1.subs({s:5}) == StateSpace(Matrix([[5]]), Matrix([[36]]), Matrix([[24]]), Matrix([[10]]))
    assert ss2.subs({p:1}) == StateSpace(Matrix([[s + 1]]), Matrix([[0]]), Matrix([[1 - s**3]]), Matrix([[s - 1]]))

    # xreplace
    assert ss1.xreplace({s:p}) == \
        StateSpace(Matrix([[p]]), Matrix([[(p + 1)**2]]), Matrix([[p**2 - 1]]), Matrix([[2*p]]))
    assert ss2.xreplace({s:a, p:b}) == \
        StateSpace(Matrix([[a + b]]), Matrix([[(a + 1)*(b - 1)]]), Matrix([[-a**3 + b**3]]), Matrix([[a - b]]))

    # evalf
    p1 = a1*s + a0
    p2 = b2*s**2 + b1*s + b0
    G = StateSpace(Matrix([p1]), Matrix([p2]))
    expect = StateSpace(Matrix([[2*s + 1]]), Matrix([[5*s**2 + 4*s + 3]]), Matrix([[0]]), Matrix([[0]]))
    expect_ = StateSpace(Matrix([[2.0*s + 1.0]]), Matrix([[5.0*s**2 + 4.0*s + 3.0]]), Matrix([[0]]), Matrix([[0]]))
    assert G.subs({a0: 1, a1: 2, b0: 3, b1: 4, b2: 5}) == expect
    assert G.subs({a0: 1, a1: 2, b0: 3, b1: 4, b2: 5}).evalf() == expect_
    assert expect.evalf() == expect_

