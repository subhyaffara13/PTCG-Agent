
def test_closed_fixed(closed, arithmetic_win_operators):
    # GH 34315
    func_name = arithmetic_win_operators
    df_fixed = DataFrame({"A": [0, 1, 2, 3, 4]})
    df_time = DataFrame({"A": [0, 1, 2, 3, 4]}, index=date_range("2020", periods=5))

    result = getattr(
        df_fixed.rolling(2, closed=closed, min_periods=1),
        func_name,
    )()
    expected = getattr(
        df_time.rolling("2D", closed=closed, min_periods=1),
        func_name,
    )().reset_index(drop=True)

    tm.assert_frame_equal(result, expected)

