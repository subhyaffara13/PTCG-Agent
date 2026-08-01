
def test_stat_method(pandasmethname, kwargs):
    s = pd.Series(data=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, pd.NA, pd.NA], dtype="Float64")
    pandasmeth = getattr(s, pandasmethname)
    result = pandasmeth(**kwargs)
    s2 = pd.Series(data=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6], dtype="float64")
    pandasmeth = getattr(s2, pandasmethname)
    expected = pandasmeth(**kwargs)
    assert expected == result


def test_stat_method(pandasmethname, kwargs):
    s = pd.Series(data=[1, 2, 3, 4, 5, 6, pd.NA, pd.NA], dtype="Int64")
    pandasmeth = getattr(s, pandasmethname)
    result = pandasmeth(**kwargs)
    s2 = pd.Series(data=[1, 2, 3, 4, 5, 6], dtype="Int64")
    pandasmeth = getattr(s2, pandasmethname)
    expected = pandasmeth(**kwargs)
    assert expected == result

