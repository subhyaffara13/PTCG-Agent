
def test_milp_optional_args():
    # check that arguments other than `c` are indeed optional
    res = milp(1)
    assert res.fun == 0
    assert_array_equal(res.x, [0])

