
def test_uselogcombine():
    eq = z - log(x) + log(y/(x*(-1 + y**2/x**2)))
    assert solve(eq, x, force=True) == [-sqrt(y*(y - exp(z))), sqrt(y*(y - exp(z)))]
    assert solve(log(x + 3) + log(1 + 3/x) - 3) in [
        [-3 + sqrt(-12 + exp(3))*exp(Rational(3, 2))/2 + exp(3)/2,
        -sqrt(-12 + exp(3))*exp(Rational(3, 2))/2 - 3 + exp(3)/2],
        [-3 + sqrt(-36 + (-exp(3) + 6)**2)/2 + exp(3)/2,
        -3 - sqrt(-36 + (-exp(3) + 6)**2)/2 + exp(3)/2],
        ]
    assert solve(log(exp(2*x) + 1) + log(-tanh(x) + 1) - log(2)) == []

