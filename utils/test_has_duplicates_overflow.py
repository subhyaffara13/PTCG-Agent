
def test_has_duplicates_overflow(nlevels, with_nulls):
    # handle int64 overflow if possible
    # no overflow with 4
    # overflow possible with 8
    codes = np.tile(np.arange(500), 2)
    level = np.arange(500)

    if with_nulls:  # inject some null values
        codes[500] = -1  # common nan value
        codes = [codes.copy() for i in range(nlevels)]
        for i in range(nlevels):
            codes[i][500 + i - nlevels // 2] = -1

        codes += [np.array([-1, 1]).repeat(500)]
    else:
        codes = [codes] * nlevels + [np.arange(2).repeat(500)]

    levels = [level] * nlevels + [[0, 1]]

    # no dups
    mi = MultiIndex(levels=levels, codes=codes)
    assert not mi.has_duplicates

    # with a dup
    if with_nulls:

        def f(a):
            return np.insert(a, 1000, a[0])

        codes = list(map(f, codes))
        mi = MultiIndex(levels=levels, codes=codes)
    else:
        values = mi.values.tolist()
        mi = MultiIndex.from_tuples([*values, values[0]])

    assert mi.has_duplicates

