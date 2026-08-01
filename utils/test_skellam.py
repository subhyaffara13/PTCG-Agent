
def test_skellam():
    mu1 = Symbol('mu1')
    mu2 = Symbol('mu2')
    z = Symbol('z')
    X = Skellam('x', mu1, mu2)

    assert density(X)(z) == (mu1/mu2)**(z/2) * \
        exp(-mu1 - mu2)*besseli(z, 2*sqrt(mu1*mu2))
    assert skewness(X).expand() == mu1/(mu1*sqrt(mu1 + mu2) + mu2 *
                sqrt(mu1 + mu2)) - mu2/(mu1*sqrt(mu1 + mu2) + mu2*sqrt(mu1 + mu2))
    assert variance(X).expand() == mu1 + mu2
    assert E(X) == mu1 - mu2
    assert characteristic_function(X)(z) == exp(
        mu1*exp(I*z) - mu1 - mu2 + mu2*exp(-I*z))
    assert moment_generating_function(X)(z) == exp(
        mu1*exp(z) - mu1 - mu2 + mu2*exp(-z))

