
def test_fancy_indexing(string_list):
    sarr = np.array(string_list, dtype="T")
    assert_array_equal(sarr, sarr[np.arange(sarr.shape[0])])

    inds = [
        [True, True],
        [0, 1],
        ...,
        np.array([0, 1], dtype='uint8'),
    ]

    lops = [
        ['a' * 25, 'b' * 25],
        ['', ''],
        ['hello', 'world'],
        ['hello', 'world' * 25],
    ]

    # see gh-27003 and gh-27053
    for ind in inds:
        for lop in lops:
            a = np.array(lop, dtype="T")
            assert_array_equal(a[ind], a)
            rop = ['d' * 25, 'e' * 25]
            for b in [rop, np.array(rop, dtype="T")]:
                a[ind] = b
                assert_array_equal(a, b)
                assert a[0] == 'd' * 25

    # see gh-29279
    data = [
        ["AAAAAAAAAAAAAAAAA"],
        ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        ["CCCCCCCCCCCCCCCCC"],
        ["DDDDDDDDDDDDDDDDD"],
    ]
    sarr = np.array(data, dtype=np.dtypes.StringDType())
    uarr = np.array(data, dtype="U30")
    for ind in [[0], [1], [2], [3], [[0, 0]], [[1, 1, 3]], [[1, 1]]]:
        assert_array_equal(sarr[ind], uarr[ind])


def test_fancy_indexing():
    # The matrix class messes with the shape. While this is always
    # weird (getitem is not used, it does not have setitem nor knows
    # about fancy indexing), this tests gh-3110
    # 2018-04-29: moved here from core.tests.test_index.
    m = np.matrix([[1, 2], [3, 4]])

    assert_(isinstance(m[[0, 1, 0], :], np.matrix))

    # gh-3110. Note the transpose currently because matrices do *not*
    # support dimension fixing for fancy indexing correctly.
    x = np.asmatrix(np.arange(50).reshape(5, 10))
    assert_equal(x[:2, np.array(-1)], x[:2, -1].T)

