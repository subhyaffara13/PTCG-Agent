
def test_is_valid_joint_degree():
    """Tests for conditions that invalidate a joint degree dict"""

    # valid joint degree that satisfies all five conditions
    joint_degrees = {
        1: {4: 1},
        2: {2: 2, 3: 2, 4: 2},
        3: {2: 2, 4: 1},
        4: {1: 1, 2: 2, 3: 1},
    }
    assert is_valid_joint_degree(joint_degrees)

    # test condition 1
    # joint_degrees_1[1][4] not integer
    joint_degrees_1 = {
        1: {4: 1.5},
        2: {2: 2, 3: 2, 4: 2},
        3: {2: 2, 4: 1},
        4: {1: 1.5, 2: 2, 3: 1},
    }
    assert not is_valid_joint_degree(joint_degrees_1)

    # test condition 2
    # degree_count[2] = sum(joint_degrees_2[2][j)/2, is not an int
    # degree_count[4] = sum(joint_degrees_2[4][j)/4, is not an int
    joint_degrees_2 = {
        1: {4: 1},
        2: {2: 2, 3: 2, 4: 3},
        3: {2: 2, 4: 1},
        4: {1: 1, 2: 3, 3: 1},
    }
    assert not is_valid_joint_degree(joint_degrees_2)

    # test conditions 3 and 4
    # joint_degrees_3[1][4]>degree_count[1]*degree_count[4]
    joint_degrees_3 = {
        1: {4: 2},
        2: {2: 2, 3: 2, 4: 2},
        3: {2: 2, 4: 1},
        4: {1: 2, 2: 2, 3: 1},
    }
    assert not is_valid_joint_degree(joint_degrees_3)

    # test condition 5
    # joint_degrees_5[1][1] not even
    joint_degrees_5 = {1: {1: 9}}
    assert not is_valid_joint_degree(joint_degrees_5)

