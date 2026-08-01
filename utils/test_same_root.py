
def test_same_root():
    f = Poly(x**4 + x**3 + x**2 + x + 1)
    eq = f.same_root
    r0 = exp(2 * I * pi / 5)
    assert [i for i, r in enumerate(f.all_roots()) if eq(r, r0)] == [3]

    raises(PolynomialError,
           lambda: Poly(x + 1, domain=QQ).same_root(0, 0))
    raises(DomainError,
           lambda: Poly(x**2 + 1, domain=FF(7)).same_root(0, 0))
    raises(DomainError,
           lambda: Poly(x ** 2 + 1, domain=ZZ_I).same_root(0, 0))
    raises(DomainError,
           lambda: Poly(y * x**2 + 1, domain=ZZ[y]).same_root(0, 0))
    raises(MultivariatePolynomialError,
           lambda: Poly(x * y + 1, domain=ZZ).same_root(0, 0))

