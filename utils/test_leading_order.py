
def test_leading_order():
    assert (x + 1 + 1/x**5).extract_leading_order(x) == ((1/x**5, O(1/x**5)),)
    assert (1 + 1/x).extract_leading_order(x) == ((1/x, O(1/x)),)
    assert (1 + x).extract_leading_order(x) == ((1, O(1, x)),)
    assert (1 + x**2).extract_leading_order(x) == ((1, O(1, x)),)
    assert (2 + x**2).extract_leading_order(x) == ((2, O(1, x)),)
    assert (x + x**2).extract_leading_order(x) == ((x, O(x)),)

