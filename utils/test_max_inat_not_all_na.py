
def test_max_inat_not_all_na():
    # GH#40767 dont interpret iNaT as NaN

    # make sure we dont round iNaT+1 to iNaT
    ser = Series([1, iNaT, 2, iNaT + 1])
    gb = ser.groupby([1, 2, 3, 3])
    result = gb.min(min_count=2)

    # Note: in converting to float64, the iNaT + 1 maps to iNaT, i.e. is lossy
    expected = Series({1: np.nan, 2: np.nan, 3: iNaT + 1})
    expected.index = expected.index.astype(int)
    tm.assert_series_equal(result, expected, check_exact=True)

