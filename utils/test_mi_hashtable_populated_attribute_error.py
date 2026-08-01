
def test_mi_hashtable_populated_attribute_error(monkeypatch):
    # GH 18165
    monkeypatch.setattr(libindex, "_SIZE_CUTOFF", 50)
    r = range(50)
    df = pd.DataFrame({"a": r, "b": r}, index=MultiIndex.from_arrays([r, r]))

    msg = "'Series' object has no attribute 'foo'"
    with pytest.raises(AttributeError, match=msg):
        df["a"].foo()

