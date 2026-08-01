
def test_astype_arrow_timestamp():
    pytest.importorskip("pyarrow")
    df = DataFrame(
        {
            "a": [
                Timestamp("2020-01-01 01:01:01.000001"),
                Timestamp("2020-01-01 01:01:01.000001"),
            ]
        },
        dtype="M8[ns]",
    )
    result = df.astype("timestamp[ns][pyarrow]")
    assert not result._mgr._has_no_reference(0)
    assert np.shares_memory(get_array(df, "a"), get_array(result, "a")._pa_array)

