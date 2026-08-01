
def test_JointPSpace_marginal_distribution():
    T = MultivariateT('T', [0, 0], [[1, 0], [0, 1]], 2)
    got = marginal_distribution(T, T[1])(x)
    ans = sqrt(2)*(x**2/2 + 1)/(4*polar_lift(x**2/2 + 1)**(S(5)/2))
    assert got == ans, got
    assert integrate(marginal_distribution(T, 1)(x), (x, -oo, oo)) == 1

    t = MultivariateT('T', [0, 0, 0], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3)
    assert comp(marginal_distribution(t, 0)(1).evalf(), 0.2, .01)

