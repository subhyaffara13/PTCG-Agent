
def test_negative_counts():
    # issue 13873
    raises(ValueError, lambda: sin(x).diff(x, -1))

