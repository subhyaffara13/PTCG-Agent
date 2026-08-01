
def test_pmint_WrightOmega():
    def omega(x):
        return LambertW(exp(x))

    f = (1 + omega(x) * (2 + cos(omega(x)) * (x + omega(x))))/(1 + omega(x))/(x + omega(x))
    g = log(x + LambertW(exp(x))) + sin(LambertW(exp(x)))

    assert heurisch(f, x) == g

