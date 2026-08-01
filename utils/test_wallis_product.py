
def test_wallis_product():
    # Wallis product, given in two different forms to ensure that Product
    # can factor simple rational expressions
    A = Product(4*n**2 / (4*n**2 - 1), (n, 1, b))
    B = Product((2*n)*(2*n)/(2*n - 1)/(2*n + 1), (n, 1, b))
    R = pi*gamma(b + 1)**2/(2*gamma(b + S.Half)*gamma(b + Rational(3, 2)))
    assert simplify(A.doit()) == R
    assert simplify(B.doit()) == R

