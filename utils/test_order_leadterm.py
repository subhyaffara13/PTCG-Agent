
def test_order_leadterm():
    assert O(x**2)._eval_as_leading_term(x, None, 1) == O(x**2)

