
def test_assoc(stat, expected):
    # 2d Array
    obs1 = np.array([[12, 13, 14, 15, 16],
                     [17, 16, 18, 19, 11],
                     [9, 15, 14, 12, 11]])
    a = association(observed=obs1, method=stat)
    assert_allclose(a, expected)

