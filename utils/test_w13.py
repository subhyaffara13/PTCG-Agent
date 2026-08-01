
def test_W13():
    # Integral not calculated. Expected result is 2*(Euler_mascheroni_constant)
    r1 = integrate(1/log(x) + 1/(1 - x) - log(log(1/x)), (x, 0, 1))
    assert r1 == 2*EulerGamma

