
def test_exgaussian():
    m, z = symbols("m, z")
    s, l = symbols("s, l", positive=True)
    X = ExGaussian("x", m, s, l)

    assert density(X)(z) == l*exp(l*(l*s**2 + 2*m - 2*z)/2) *\
        erfc(sqrt(2)*(l*s**2 + m - z)/(2*s))/2

    # Note: actual_output simplifies to expected_output.
    # Ideally cdf(X)(z) would return expected_output
    # expected_output = (erf(sqrt(2)*(l*s**2 + m - z)/(2*s)) - 1)*exp(l*(l*s**2 + 2*m - 2*z)/2)/2 - erf(sqrt(2)*(m - z)/(2*s))/2 + S.Half
    u = l*(z - m)
    v = l*s
    GaussianCDF1 = cdf(Normal('x', 0, v))(u)
    GaussianCDF2 = cdf(Normal('x', v**2, v))(u)
    actual_output = GaussianCDF1 - exp(-u + (v**2/2) + log(GaussianCDF2))
    assert cdf(X)(z) == actual_output
    # assert simplify(actual_output) == expected_output

    assert variance(X).expand() == s**2 + l**(-2)

    assert skewness(X).expand() == 2/(l**3*s**2*sqrt(s**2 + l**(-2)) + l *
                                      sqrt(s**2 + l**(-2)))

