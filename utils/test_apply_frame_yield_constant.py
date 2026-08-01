
def test_apply_frame_yield_constant(df):
    # GH13568
    result = df.groupby(["A", "B"]).apply(len)
    assert isinstance(result, Series)
    assert result.name is None

    result = df.groupby(["A", "B"])[["C", "D"]].apply(len)
    assert isinstance(result, Series)
    assert result.name is None

