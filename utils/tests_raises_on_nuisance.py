import re

def tests_raises_on_nuisance(test_frame, using_infer_string):
    df = test_frame
    df["D"] = "foo"
    r = df.resample("h")
    result = r[["A", "B"]].mean()
    expected = pd.concat([r.A.mean(), r.B.mean()], axis=1)
    tm.assert_frame_equal(result, expected)

    expected = r[["A", "B", "C"]].mean()
    msg = re.escape("agg function failed [how->mean,dtype->")
    if using_infer_string:
        msg = "dtype 'str' does not support operation 'mean'"
    with pytest.raises(TypeError, match=msg):
        r.mean()
    result = r.mean(numeric_only=True)
    tm.assert_frame_equal(result, expected)

