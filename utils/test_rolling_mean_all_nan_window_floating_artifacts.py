
def test_rolling_mean_all_nan_window_floating_artifacts(start, exp_values):
    # GH#41053
    df = DataFrame(
        [
            0.03,
            0.03,
            0.001,
            np.nan,
            0.002,
            0.008,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            0.005,
            0.2,
        ]
    )

    values = [
        *exp_values,
        0.00366666,
        0.005,
        0.005,
        0.008,
        np.nan,
        np.nan,
        0.005,
        0.102500,
    ]
    expected = DataFrame(
        values,
        index=list(range(start, len(values) + start)),
    )
    result = df.iloc[start:].rolling(5, min_periods=0).mean()
    tm.assert_frame_equal(result, expected)

