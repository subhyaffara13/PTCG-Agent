
def test_gaussian_inverse():
    # test for symbolic parameters
    a, b = symbols('a b')
    assert GaussianInverse('x', a, b)

    # Inverse Gaussian distribution is also known as Wald distribution
    # `GaussianInverse` can also be referred by the name `Wald`
    a, b, z = symbols('a b z')
    X = Wald('x', a, b)
    assert density(X)(z) == sqrt(2)*sqrt(b/z**3)*exp(-b*(-a + z)**2/(2*a**2*z))/(2*sqrt(pi))

    a, b = symbols('a b', positive=True)
    z = Symbol('z', positive=True)

    X = GaussianInverse('x', a, b)
    assert density(X)(z) == sqrt(2)*sqrt(b)*sqrt(z**(-3))*exp(-b*(-a + z)**2/(2*a**2*z))/(2*sqrt(pi))
    assert E(X) == a
    assert variance(X).expand() == a**3/b
    assert cdf(X)(z) == (S.Half - erf(sqrt(2)*sqrt(b)*(1 + z/a)/(2*sqrt(z)))/2)*exp(2*b/a) +\
         erf(sqrt(2)*sqrt(b)*(-1 + z/a)/(2*sqrt(z)))/2 + S.Half

    a = symbols('a', nonpositive=True)
    raises(ValueError, lambda: GaussianInverse('x', a, b))

    a = symbols('a', positive=True)
    b = symbols('b', nonpositive=True)
    raises(ValueError, lambda: GaussianInverse('x', a, b))

