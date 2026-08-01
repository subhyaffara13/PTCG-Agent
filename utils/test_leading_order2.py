
def test_leading_order2():
    assert set((2 + pi + x**2).extract_leading_order(x)) == {(pi, O(1, x)),
            (S(2), O(1, x))}
    assert set((2*x + pi*x + x**2).extract_leading_order(x)) == {(2*x, O(x)),
            (x*pi, O(x))}

