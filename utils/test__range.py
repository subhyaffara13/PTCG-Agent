
def test_Range():
    # Only works in Python 3 where range returns a range type
    assert sympify(range(10)) == Range(10)
    assert _sympify(range(10)) == Range(10)

