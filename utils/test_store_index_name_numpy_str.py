
def test_store_index_name_numpy_str(table_format, temp_h5_path, unit, tz):
    # GH #13492
    idx = (
        DatetimeIndex(
            [dt.date(2000, 1, 1), dt.date(2000, 1, 2)],
            name="cols\u05d2",
        )
        .tz_localize(tz)
        .as_unit(unit)
    )
    idx1 = (
        DatetimeIndex(
            [dt.date(2010, 1, 1), dt.date(2010, 1, 2)],
            name="rows\u05d0",
        )
        .as_unit(unit)
        .tz_localize(tz)
    )
    df = DataFrame(np.arange(4).reshape(2, 2), columns=idx, index=idx1)

    # This used to fail, returning numpy strings instead of python strings.
    df.to_hdf(temp_h5_path, key="df", format=table_format)
    df2 = read_hdf(temp_h5_path, "df")

    tm.assert_frame_equal(df, df2, check_names=True)

    assert isinstance(df2.index.name, str)
    assert isinstance(df2.columns.name, str)

