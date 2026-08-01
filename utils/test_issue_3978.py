
def test_issue_3978():
    f = Function('f')
    assert f(x).series(x, 0, 3, dir='-') == \
            f(0) + x*Subs(Derivative(f(x), x), x, 0) + \
            x**2*Subs(Derivative(f(x), x, x), x, 0)/2 + O(x**3)
    assert f(x).series(x, 0, 3) == \
            f(0) + x*Subs(Derivative(f(x), x), x, 0) + \
            x**2*Subs(Derivative(f(x), x, x), x, 0)/2 + O(x**3)
    assert f(x**2).series(x, 0, 3) == \
            f(0) + x**2*Subs(Derivative(f(x), x), x, 0) + O(x**3)
    assert f(x**2+1).series(x, 0, 3) == \
            f(1) + x**2*Subs(Derivative(f(x), x), x, 1) + O(x**3)

    class TestF(Function):
        pass

    assert TestF(x).series(x, 0, 3) ==  TestF(0) + \
            x*Subs(Derivative(TestF(x), x), x, 0) + \
            x**2*Subs(Derivative(TestF(x), x, x), x, 0)/2 + O(x**3)

