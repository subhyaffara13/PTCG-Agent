
def test_values_multiindex_periodindex():
    # Test to ensure we hit the boxing / nobox part of MI.values
    ints = np.arange(2007, 2012)
    pidx = pd.PeriodIndex(ints, freq="D")

    idx = MultiIndex.from_arrays([ints, pidx])
    result = idx.values

    outer = Index([x[0] for x in result])
    tm.assert_index_equal(outer, Index(ints, dtype=np.int64))

    inner = pd.PeriodIndex([x[1] for x in result])
    tm.assert_index_equal(inner, pidx)

    # n_lev > n_lab
    result = idx[:2].values

    outer = Index([x[0] for x in result])
    tm.assert_index_equal(outer, Index(ints[:2], dtype=np.int64))

    inner = pd.PeriodIndex([x[1] for x in result])
    tm.assert_index_equal(inner, pidx[:2])

