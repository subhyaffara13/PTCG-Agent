
def test_npfunc_no_warnings():
    df = DataFrame({"col1": [1, 2, 3, 4, 5]})
    with tm.assert_produces_warning(False):
        df.col1.rolling(2).apply(np.prod, raw=True, engine="numba")

