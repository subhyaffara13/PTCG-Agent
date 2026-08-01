
def test_X12():
    # Look at the generalized Taylor series around x = 1
    # Result => (x - 1)^a/e^b [1 - (a + 2 b) (x - 1) / 2 + O((x - 1)^2)]
    a, b, x = symbols('a b x', real=True)
    # series returns O(log(x-1)**2)
    # https://github.com/sympy/sympy/issues/7168
    assert (series(log(x)**a*exp(-b*x), x, x0=1, n=2) ==
            (x - 1)**a/exp(b)*(1 - (a + 2*b)*(x - 1)/2 + O((x - 1)**2)))

