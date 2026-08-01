
def test_center():
    assert center('1', 2) == '1 '
    assert center('1', 3) == ' 1 '
    assert center('1', 3, '-') == '-1-'
    assert center('1', 5, '-') == '--1--'


def test_center():
    # the center of the dihedral group D_n is of order 2 for even n
    for i in (4, 6, 10):
        D = DihedralGroup(i)
        assert (D.center()).order() == 2
    # the center of the dihedral group D_n is of order 1 for odd n>2
    for i in (3, 5, 7):
        D = DihedralGroup(i)
        assert (D.center()).order() == 1
    # the center of an abelian group is the group itself
    for i in (2, 3, 5):
        for j in (1, 5, 7):
            for k in (1, 1, 11):
                G = AbelianGroup(i, j, k)
                assert G.center().is_subgroup(G)
    # the center of a nonabelian simple group is trivial
    for i in(1, 5, 9):
        A = AlternatingGroup(i)
        assert (A.center()).order() == 1
    # brute-force verifications
    D = DihedralGroup(5)
    A = AlternatingGroup(3)
    C = CyclicGroup(4)
    G.is_subgroup(D*A*C)
    assert _verify_centralizer(G, G)


def test_center(raw):
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = obj.rolling(20, min_periods=15, center=True).apply(f, raw=raw)
    expected = (
        concat([obj, Series([np.nan] * 9)])
        .rolling(20, min_periods=15)
        .apply(f, raw=raw)
        .iloc[9:]
        .reset_index(drop=True)
    )
    tm.assert_series_equal(result, expected)


def test_center(roll_func, kwargs, minp):
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = getattr(obj.rolling(20, min_periods=minp, center=True), roll_func)(
        **kwargs
    )
    expected = (
        getattr(
            concat([obj, Series([np.nan] * 9)]).rolling(20, min_periods=minp), roll_func
        )(**kwargs)
        .iloc[9:]
        .reset_index(drop=True)
    )
    tm.assert_series_equal(result, expected)


def test_center(q):
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = obj.rolling(20, center=True).quantile(q)
    expected = (
        concat([obj, Series([np.nan] * 9)])
        .rolling(20)
        .quantile(q)
        .iloc[9:]
        .reset_index(drop=True)
    )
    tm.assert_series_equal(result, expected)


def test_center(roll_func):
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = getattr(obj.rolling(20, center=True), roll_func)()
    expected = (
        getattr(concat([obj, Series([np.nan] * 9)]).rolling(20), roll_func)()
        .iloc[9:]
        .reset_index(drop=True)
    )
    tm.assert_series_equal(result, expected)

