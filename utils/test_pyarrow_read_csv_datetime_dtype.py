
def test_pyarrow_read_csv_datetime_dtype():
    # GH 59904
    data = '"date"\n"20/12/2025"\n""\n"31/12/2020"'
    result = pd.read_csv(
        StringIO(data), parse_dates=["date"], dayfirst=True, dtype_backend="pyarrow"
    )

    expect_data = pd.to_datetime(["20/12/2025", pd.NaT, "31/12/2020"], dayfirst=True)
    expect = pd.DataFrame({"date": expect_data})

    tm.assert_frame_equal(expect, result)

