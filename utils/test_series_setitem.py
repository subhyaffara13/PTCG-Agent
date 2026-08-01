
def test_series_setitem(indexer):
    # ensure we only get a single warning for those typical cases of chained
    # assignment
    df = DataFrame({"a": [1, 2, 3], "b": 1})

    # using custom check instead of tm.assert_produces_warning because that doesn't
    # fail if multiple warnings are raised
    if CHAINED_WARNING_DISABLED:
        return
    with pytest.warns() as record:  # noqa: TID251
        df["a"][indexer] = 0
    assert len(record) == 1
    assert record[0].category == ChainedAssignmentError

