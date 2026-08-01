
def test_order_failing_due_to_solveset():
    assert O(x**3).subs(x, exp(-x**2)) == O(exp(-3*x**2), (x, -oo))
    raises(NotImplementedError, lambda: O(x).subs(x, O(1/x))) # mixing of order at different points

