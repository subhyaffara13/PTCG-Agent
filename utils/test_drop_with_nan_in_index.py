
def test_drop_with_nan_in_index(nulls_fixture):
    # GH#18853
    mi = MultiIndex.from_tuples([("blah", nulls_fixture)], names=["name", "date"])
    msg = r"labels \[Timestamp\('2001-01-01 00:00:00'\)\] not found in level"
    with pytest.raises(KeyError, match=msg):
        mi.drop(pd.Timestamp("2001"), level="date")

