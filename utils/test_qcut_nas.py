
def test_qcut_nas():
    arr = np.random.default_rng(2).standard_normal(100)
    arr[:20] = np.nan

    result = qcut(arr, 4)
    assert isna(result[:20]).all()

