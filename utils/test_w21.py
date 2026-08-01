
def test_W21():
    assert abs(N(integrate(x**2*polylog(3, 1/(x + 1)), (x, 0, 1)))
        - 0.210882859565594) < 1e-15

