
def test_fancy_getitem():
    dti = date_range(
        freq="WOM-1FRI", start=datetime(2005, 1, 1), end=datetime(2010, 1, 1)
    )

    s = Series(np.arange(len(dti)), index=dti)

    assert s["1/2/2009"] == 48
    assert s["2009-1-2"] == 48
    assert s[datetime(2009, 1, 2)] == 48
    assert s[Timestamp(datetime(2009, 1, 2))] == 48
    with pytest.raises(KeyError, match=r"^'2009-1-3'$"):
        s["2009-1-3"]
    tm.assert_series_equal(
        s["3/6/2009":"2009-06-05"], s[datetime(2009, 3, 6) : datetime(2009, 6, 5)]
    )

