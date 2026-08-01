
def test_methods_std_var(f, test_frame):
    g = test_frame.groupby("A")
    r = g.resample("2s")
    result = getattr(r, f)(ddof=1)
    expected = g.apply(lambda x: getattr(x.resample("2s"), f)(ddof=1))
    tm.assert_frame_equal(result, expected)

