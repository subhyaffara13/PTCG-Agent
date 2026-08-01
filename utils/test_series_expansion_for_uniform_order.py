
def test_series_expansion_for_uniform_order():
    assert (1/x + y + x).series(x, 0, 0) == 1/x + O(1, x)
    assert (1/x + y + x).series(x, 0, 1) == 1/x + y + O(x)
    assert (1/x + 1 + x).series(x, 0, 0) == 1/x + O(1, x)
    assert (1/x + 1 + x).series(x, 0, 1) == 1/x + 1 + O(x)
    assert (1/x + x).series(x, 0, 0) == 1/x + O(1, x)
    assert (1/x + y + y*x + x).series(x, 0, 0) == 1/x + O(1, x)
    assert (1/x + y + y*x + x).series(x, 0, 1) == 1/x + y + O(x)

