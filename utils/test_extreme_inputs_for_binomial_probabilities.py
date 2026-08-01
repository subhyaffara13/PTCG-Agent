
def test_extreme_inputs_for_binomial_probabilities(func, dtype):
    # certain inputs caused C++ exceptions in boost
    # resulting in Python interpreter crashes
    k = 3e18
    n = 10e18
    p = 0.3
    func(dtype(k), dtype(n), dtype(p))

