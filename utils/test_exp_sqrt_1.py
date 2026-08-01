
def test_exp_sqrt_1():
    assert exp(1 + sqrt(x)).nseries(x, n=3) ==  \
        (exp(1)*(1 + sqrt(x) + x/2 + sqrt(x)*x/6)).expand() + O(sqrt(x)**3)

