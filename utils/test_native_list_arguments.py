
def test_native_list_arguments():
    c = [1,2,4,7]
    r = [1,3,9,12]
    y = [5,1,4,2]
    actual = solve_toeplitz((c,r), y)
    desired = solve(toeplitz(c, r=r), y)
    assert_allclose(actual, desired)

