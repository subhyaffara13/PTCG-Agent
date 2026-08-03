import re

def test_issue_15432():
    assert integrate(x**n * exp(-x) * log(x), (x, 0, oo)).gammasimp() == Piecewise(
        (gamma(n + 1)*polygamma(0, n) + gamma(n + 1)/n, re(n) + 1 > 0),
        (Integral(x**n*exp(-x)*log(x), (x, 0, oo)), True))

