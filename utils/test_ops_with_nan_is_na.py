
def test_ops_with_nan_is_na(using_nan_is_na):
    # GH#61732
    ser = pd.Series([-1, 0, 1], dtype="int64[pyarrow]")

    result = ser - np.nan
    if using_nan_is_na:
        assert result.isna().all()
    else:
        assert not result.isna().any()

    result = ser * np.nan
    if using_nan_is_na:
        assert result.isna().all()
    else:
        assert not result.isna().any()

    result = ser / 0
    if using_nan_is_na:
        assert result.isna()[1]
    else:
        assert not result.isna()[1]

