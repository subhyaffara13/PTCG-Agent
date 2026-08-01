
def test_safe_first_element_pandas_series(pd):
    # deliberately create a pandas series with index not starting from 0
    s = pd.Series(range(5), index=range(10, 15))
    actual = cbook._safe_first_finite(s)
    assert actual == 0

