
def test_latex_RandomDomain():
    from sympy.stats import Normal, Die, Exponential, pspace, where
    from sympy.stats.rv import RandomDomain

    X = Normal('x1', 0, 1)
    assert latex(where(X > 0)) == r"\text{Domain: }0 < x_{1} \wedge x_{1} < \infty"

    D = Die('d1', 6)
    assert latex(where(D > 4)) == r"\text{Domain: }d_{1} = 5 \vee d_{1} = 6"

    A = Exponential('a', 1)
    B = Exponential('b', 1)
    assert latex(
        pspace(Tuple(A, B)).domain) == \
        r"\text{Domain: }0 \leq a \wedge 0 \leq b \wedge a < \infty \wedge b < \infty"

    assert latex(RandomDomain(FiniteSet(x), FiniteSet(1, 2))) == \
        r'\text{Domain: }\left\{x\right\} \in \left\{1, 2\right\}'

