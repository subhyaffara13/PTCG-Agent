
def test_timestamp_ns_pyarrow():
    # GH 56712
    pytest.importorskip("pyarrow", "11.0.0")
    timestamp_args = {
        "year": 2000,
        "month": 1,
        "day": 1,
        "hour": 1,
        "minute": 1,
        "second": 1,
    }
    df = pd.Series(
        [datetime(**timestamp_args)],
        dtype="timestamp[ns][pyarrow]",
        name="col0",
    ).to_frame()

    with tm.assert_produces_warning(match="Interchange"):
        dfi = df.__dataframe__()
        result = pd.api.interchange.from_dataframe(dfi)["col0"].item()

    expected = pd.Timestamp(**timestamp_args)
    assert result == expected

