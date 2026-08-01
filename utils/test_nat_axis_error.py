
def test_nat_axis_error():
    idx = [Timestamp("2020"), NaT]
    df = DataFrame(np.eye(2), index=idx)
    with pytest.raises(ValueError, match="index values must not have NaT"):
        df.rolling("D").mean()

