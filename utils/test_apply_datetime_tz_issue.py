
def test_apply_datetime_tz_issue(engine, request):
    # GH 29052

    if engine == "numba":
        mark = pytest.mark.xfail(
            reason="numba engine doesn't support non-numeric indexes"
        )
        request.node.add_marker(mark)

    timestamps = [
        Timestamp("2019-03-15 12:34:31.909000+0000", tz="UTC"),
        Timestamp("2019-03-15 12:34:34.359000+0000", tz="UTC"),
        Timestamp("2019-03-15 12:34:34.660000+0000", tz="UTC"),
    ]
    df = DataFrame(data=[0, 1, 2], index=timestamps)
    result = df.apply(lambda x: x.name, axis=1, engine=engine)
    expected = Series(index=timestamps, data=timestamps)

    tm.assert_series_equal(result, expected)

