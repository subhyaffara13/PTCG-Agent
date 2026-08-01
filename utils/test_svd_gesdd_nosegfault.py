
def test_svd_gesdd_nosegfault():
    # svd(a) with {U,VT}.size > INT_MAX does not segfault
    # cf https://github.com/scipy/scipy/issues/14001
    check_free_memory(free_mb=19_000)
    df=np.ones((4799, 53130), dtype=np.float64)
    with assert_raises(ValueError):
        svd(df)

