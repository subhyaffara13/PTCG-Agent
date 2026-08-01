
def test_evalf_mul():
    # SymPy should not try to expand this; it should be handled term-wise
    # in evalf through mpmath
    assert NS(product(1 + sqrt(n)*I, (n, 1, 500)), 1) == '5.e+567 + 2.e+568*I'

