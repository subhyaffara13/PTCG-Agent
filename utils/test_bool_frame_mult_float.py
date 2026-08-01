
def test_bool_frame_mult_float():
    # GH 18549
    df = DataFrame(True, list("ab"), list("cd"))
    result = df * 1.0
    expected = DataFrame(np.ones((2, 2)), list("ab"), list("cd"))
    tm.assert_frame_equal(result, expected)

