
def test_nested_structured_subarray():
    # Test from gh-16678
    point = np.dtype([('x', float), ('y', float)])
    dt = np.dtype([('code', int), ('points', point, (2,))])
    data = StringIO("100,1,2,3,4\n200,5,6,7,8\n")
    expected = np.array(
        [
            (100, [(1., 2.), (3., 4.)]),
            (200, [(5., 6.), (7., 8.)]),
        ],
        dtype=dt
    )
    assert_array_equal(np.loadtxt(data, dtype=dt, delimiter=","), expected)

