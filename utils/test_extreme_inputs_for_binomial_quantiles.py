
def test_extreme_inputs_for_binomial_quantiles(func, dtype):
    # certain inputs caused C++ exceptions in boost
    # resulting in Python interpreter crashes
    n = 10e18
    p = 0.5
    func(dtype(p), dtype(n), dtype(p))

