
def test_reindex_datetimeindexes_tz_naive_and_aware():
    # GH 8306
    idx = date_range("20131101", tz="America/Chicago", periods=7, unit="ns")
    newidx = date_range("20131103", periods=10, freq="h", unit="ns")
    s = Series(range(7), index=idx)
    msg = (
        r"Cannot compare dtypes datetime64\[ns, America/Chicago\] "
        r"and datetime64\[ns\]"
    )
    with pytest.raises(TypeError, match=msg):
        s.reindex(newidx, method="ffill")

