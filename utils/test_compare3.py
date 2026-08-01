
def test_compare3():
    assert compare(exp(exp(x)), exp(x + exp(-exp(x))), x) == ">"

