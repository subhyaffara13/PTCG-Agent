
def test_api(_test_series):
    r = _test_series.resample("h")
    result = r.mean()
    assert isinstance(result, Series)
    assert len(result) == 217

    r = _test_series.to_frame().resample("h")
    result = r.mean()
    assert isinstance(result, DataFrame)
    assert len(result) == 217


def test_api(any_string_dtype):
    # GH 6106, GH 9322
    assert Series.str is StringMethods
    assert isinstance(Series([""], dtype=any_string_dtype).str, StringMethods)


def test_api(temp_h5_path):
    # GH4584
    # API issue when to_hdf doesn't accept append AND format args
    path = temp_h5_path

    df = DataFrame(range(20))
    df.iloc[:10].to_hdf(path, key="df", append=True, format="table")
    df.iloc[10:].to_hdf(path, key="df", append=True, format="table")
    tm.assert_frame_equal(read_hdf(path, "df"), df)

    # append to False
    df.iloc[:10].to_hdf(path, key="df", append=False, format="table")
    df.iloc[10:].to_hdf(path, key="df", append=True, format="table")
    tm.assert_frame_equal(read_hdf(path, "df"), df)

