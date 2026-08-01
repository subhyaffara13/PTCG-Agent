
def test_expanding():
    # see gh-23372.
    df = DataFrame(np.ones((10, 20)))

    expected = DataFrame(
        {i: [np.nan] * 2 + [float(j) for j in range(3, 11)] for i in range(20)}
    )
    result = df.expanding(3).sum()
    tm.assert_frame_equal(result, expected)

