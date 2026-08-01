
def test_binary_frame_series_raises():
    # We don't currently implement
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(NotImplementedError, match="logaddexp"):
        np.logaddexp(df, df["A"])

    with pytest.raises(NotImplementedError, match="logaddexp"):
        np.logaddexp(df["A"], df)

