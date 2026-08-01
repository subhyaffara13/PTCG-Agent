
def test_group_columns():
    structure = [
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0]
    ]
    for transform in [np.asarray, csr_array, csc_array, lil_array]:
        A = transform(structure)
        order = np.arange(6)
        groups_true = np.array([0, 1, 2, 0, 1, 2])
        groups = group_columns(A, order)
        assert_equal(groups, groups_true)

        order = [1, 2, 4, 3, 5, 0]
        groups_true = np.array([2, 0, 1, 2, 0, 1])
        groups = group_columns(A, order)
        assert_equal(groups, groups_true)

    # Test repeatability.
    groups_1 = group_columns(A)
    groups_2 = group_columns(A)
    assert_equal(groups_1, groups_2)

