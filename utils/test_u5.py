
def test_U5():
    # issue 6681
    t = symbols('t')
    ans = (
        Derivative(f(g(t)), g(t))*Derivative(g(t), (t, 2)) +
        Derivative(f(g(t)), (g(t), 2))*Derivative(g(t), t)**2)
    assert f(g(t)).diff(t, 2) == ans
    assert ans.doit() == ans

