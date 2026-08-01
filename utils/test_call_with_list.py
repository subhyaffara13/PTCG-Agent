
def test_call_with_list(Poly):
    p = Poly([1, 2, 3])
    x = [-1, 0, 2]
    res = p(x)
    assert_equal(res, p(np.array(x)))

