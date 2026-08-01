
def test_is_valid_directed_joint_degree():
    in_degrees = [0, 1, 1, 2]
    out_degrees = [1, 1, 1, 1]
    nkk = {1: {1: 2, 2: 2}}
    assert is_valid_directed_joint_degree(in_degrees, out_degrees, nkk)

    # not realizable, values are not integers.
    nkk = {1: {1: 1.5, 2: 2.5}}
    assert not is_valid_directed_joint_degree(in_degrees, out_degrees, nkk)

    # not realizable, number of edges between 1-2 are insufficient.
    nkk = {1: {1: 2, 2: 1}}
    assert not is_valid_directed_joint_degree(in_degrees, out_degrees, nkk)

    # not realizable, in/out degree sequences have different number of nodes.
    out_degrees = [1, 1, 1]
    nkk = {1: {1: 2, 2: 2}}
    assert not is_valid_directed_joint_degree(in_degrees, out_degrees, nkk)

    # not realizable, degree sequences have fewer than required nodes.
    in_degrees = [0, 1, 2]
    assert not is_valid_directed_joint_degree(in_degrees, out_degrees, nkk)

