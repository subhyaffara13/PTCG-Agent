
def test_T4():
    assert limit((exp(x*exp(-x)/(exp(-x) + exp(-2*x**2/(x + 1))))
                 - exp(x))/x, x, oo) == -exp(2)

