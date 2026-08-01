
def test_stdtr_stdtri_invalid():
    # a mix of large and inf df with t/p equal to nan
    df = [1e10, 1e12, 1e120, np.inf]
    x = np.nan
    res1 = stdtr(df, x)
    res2 = stdtrit(df, x)
    res_ex = 4*[np.nan]
    assert_equal(res1, res_ex)
    assert_equal(res2, res_ex)

