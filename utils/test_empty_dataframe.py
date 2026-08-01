
def test_empty_dataframe():
    df = DataFrame()
    arr = np.asarray(df)
    assert arr.flags.writeable is True


def test_empty_dataframe():
    # https://github.com/pandas-dev/pandas/issues/56700
    df = pd.DataFrame({"a": []}, dtype="int8")
    with tm.assert_produces_warning(match="Interchange"):
        dfi = df.__dataframe__()
        result = pd.api.interchange.from_dataframe(dfi, allow_copy=False)
    expected = pd.DataFrame({"a": []}, dtype="int8")
    tm.assert_frame_equal(result, expected)


def test_empty_dataframe():
    df = DataFrame({"A": []})
    result = df.to_csv(float_format="{:.2f}", lineterminator="\n")
    expected = ",A\n"
    assert result == expected

