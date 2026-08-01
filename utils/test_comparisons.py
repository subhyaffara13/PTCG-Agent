
def test_comparisons(string_list, dtype, op, o_dtype):
    sarr = np.array(string_list, dtype=dtype)
    oarr = np.array(string_list, dtype=o_dtype)

    # test that comparison operators work
    res = op(sarr, sarr)
    ores = op(oarr, oarr)
    # test that promotion works as well
    orres = op(sarr, oarr)
    olres = op(oarr, sarr)

    assert_array_equal(res, ores)
    assert_array_equal(res, orres)
    assert_array_equal(res, olres)

    # test we get the correct answer for unequal length strings
    sarr2 = np.array([s + "2" for s in string_list], dtype=dtype)
    oarr2 = np.array([s + "2" for s in string_list], dtype=o_dtype)

    res = op(sarr, sarr2)
    ores = op(oarr, oarr2)
    olres = op(oarr, sarr2)
    orres = op(sarr, oarr2)

    assert_array_equal(res, ores)
    assert_array_equal(res, olres)
    assert_array_equal(res, orres)

    res = op(sarr2, sarr)
    ores = op(oarr2, oarr)
    olres = op(oarr2, sarr)
    orres = op(sarr2, oarr)

    assert_array_equal(res, ores)
    assert_array_equal(res, olres)
    assert_array_equal(res, orres)

