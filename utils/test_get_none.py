
def test_get_none():
    # GH#5652
    s1 = Series(dtype=object)
    s2 = Series(dtype=object, index=list("abc"))
    for s in [s1, s2]:
        result = s.get(None)
        assert result is None

