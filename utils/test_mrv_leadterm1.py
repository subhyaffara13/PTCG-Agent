
def test_mrv_leadterm1():
    assert mrv_leadterm(-exp(1/x), x) == (-1, 0)
    assert mrv_leadterm(1/exp(-x + exp(-x)) - exp(x), x) == (-1, 0)
    assert mrv_leadterm(
        (exp(1/x - exp(-x)) - exp(1/x))*exp(x), x) == (-exp(1/x), 0)

