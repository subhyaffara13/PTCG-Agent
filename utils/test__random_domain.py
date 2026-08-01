
def test_RandomDomain():
    from sympy.stats import Normal, Die, Exponential, pspace, where
    X = Normal('x1', 0, 1)
    assert str(where(X > 0)) == "Domain: (0 < x1) & (x1 < oo)"

    D = Die('d1', 6)
    assert str(where(D > 4)) == "Domain: Eq(d1, 5) | Eq(d1, 6)"

    A = Exponential('a', 1)
    B = Exponential('b', 1)
    assert str(pspace(Tuple(A, B)).domain) == "Domain: (0 <= a) & (0 <= b) & (a < oo) & (b < oo)"


def test_RandomDomain():
    from sympy.stats import Normal, Die, Exponential, pspace, where
    X = Normal('x1', 0, 1)
    assert upretty(where(X > 0)) == "Domain: 0 < x₁ ∧ x₁ < ∞"

    D = Die('d1', 6)
    assert upretty(where(D > 4)) == 'Domain: d₁ = 5 ∨ d₁ = 6'

    A = Exponential('a', 1)
    B = Exponential('b', 1)
    assert upretty(pspace(Tuple(A, B)).domain) == \
        'Domain: 0 ≤ a ∧ 0 ≤ b ∧ a < ∞ ∧ b < ∞'

