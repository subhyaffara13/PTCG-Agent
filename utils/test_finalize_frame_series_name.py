
def test_finalize_frame_series_name():
    # https://github.com/pandas-dev/pandas/pull/37186/files#r506978889
    # ensure we don't copy the column `name` to the Series.
    df = pd.DataFrame({"name": [1, 2]})
    result = pd.Series([1, 2]).__finalize__(df)
    assert result.name is None

