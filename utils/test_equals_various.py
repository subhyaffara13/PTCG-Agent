
def test_equals_various(other):
    df = DataFrame({"A": ["a", "b", "c"]}, dtype=object)
    result = df.eval(f"A == {other}")
    expected = Series([False, False, False], name="A")
    tm.assert_series_equal(result, expected)

