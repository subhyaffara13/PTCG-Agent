
def test_retain_index_attributes2(temp_h5_path):
    with tm.assert_produces_warning(errors.AttributeConflictWarning):
        df = DataFrame(
            {"A": Series(range(3), index=date_range("2000-1-1", periods=3, freq="h"))}
        )
        df.to_hdf(temp_h5_path, key="data", mode="w", append=True)
        df2 = DataFrame(
            {"A": Series(range(3), index=date_range("2002-1-1", periods=3, freq="D"))}
        )

        df2.to_hdf(temp_h5_path, key="data", append=True)

        idx = date_range("2000-1-1", periods=3, freq="h")
        idx.name = "foo"
        df = DataFrame({"A": Series(range(3), index=idx)})
        df.to_hdf(temp_h5_path, key="data", mode="w", append=True)

    assert read_hdf(temp_h5_path, key="data").index.name == "foo"

    with tm.assert_produces_warning(errors.AttributeConflictWarning):
        idx2 = date_range("2001-1-1", periods=3, freq="h")
        idx2.name = "bar"
        df2 = DataFrame({"A": Series(range(3), index=idx2)})
        df2.to_hdf(temp_h5_path, key="data", append=True)

    assert read_hdf(temp_h5_path, "data").index.name is None

