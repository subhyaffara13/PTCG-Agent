
def test_exp_2():
    assert exp(x**3).nseries(x, 0, 14) == 1 + x**3 + x**6/2 + x**9/6 + x**12/24 + O(x**14)

