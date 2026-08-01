
def test_canberra():
    # Regression test for ticket #1430.
    assert_equal(wcanberra([1, 2, 3], [2, 4, 6]), 1)
    assert_equal(wcanberra([1, 1, 0, 0], [1, 0, 1, 0]), 2)

