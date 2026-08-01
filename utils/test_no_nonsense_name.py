
def test_no_nonsense_name(float_frame):
    # GH #995
    s = float_frame["C"].copy()
    s.name = None

    result = s.groupby(float_frame["A"]).agg("sum")
    assert result.name is None

