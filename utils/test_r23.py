
def test_R23():
    n, k = symbols('n k', integer=True, positive=True)
    Sm = Sum(Sum((factorial(n)/(factorial(k)**2*factorial(n - 2*k)))*
                 (x/y)**k*(x*y)**(n - k), (n, 2*k, oo)), (k, 0, oo))
    # Missing how to express constraint abs(x*y)<1?
    T = Sm.doit()  # Sum not calculated
    assert T == -1/sqrt(x**2*y**2 - 4*x**2 - 2*x*y + 1)

