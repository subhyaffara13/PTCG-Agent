
def test_groupby():
    assert groupby(iseven, [1, 2, 3, 4]) == {True: [2, 4], False: [1, 3]}


def test_groupby(idx):
    groups = idx.groupby(np.array([1, 1, 1, 2, 2, 2]))
    labels = idx.tolist()
    exp = {1: labels[:3], 2: labels[3:]}
    tm.assert_dict_equal(groups, exp)

    # GH5620
    groups = idx.groupby(idx)
    exp = {key: [key] for key in idx}
    tm.assert_dict_equal(groups, exp)

