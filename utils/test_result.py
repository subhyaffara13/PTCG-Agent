
def test_result():
    res = crosstab([0, 1], [1, 2])
    assert_equal((res.elements, res.count), res)


def test_result():
    A, b, c, numbers, M = magic_square(3)
    res = milp(c=c, constraints=(A, b, b), bounds=(0, 1), integrality=1)
    assert res.status == 0
    assert res.success
    msg = "Optimization terminated successfully. (HiGHS Status 7:"
    assert res.message.startswith(msg)
    assert isinstance(res.x, np.ndarray)
    assert isinstance(res.fun, float)
    assert isinstance(res.mip_node_count, int)
    assert isinstance(res.mip_dual_bound, float)
    assert isinstance(res.mip_gap, float)

    A, b, c, numbers, M = magic_square(6)
    res = milp(c=c*0, constraints=(A, b, b), bounds=(0, 1), integrality=1,
               options={'time_limit': 0.05})
    assert res.status == 1
    assert not res.success
    msg = "Time limit reached. (HiGHS Status 13:"
    assert res.message.startswith(msg)
    assert (res.fun is res.mip_dual_bound is res.mip_gap
            is res.mip_node_count is res.x is None)

    res = milp(1, bounds=(1, -1))
    assert res.status == 2
    assert not res.success
    msg = "The problem is infeasible. (HiGHS Status 8:"
    assert res.message.startswith(msg)
    assert (res.fun is res.mip_dual_bound is res.mip_gap
            is res.mip_node_count is res.x is None)

    res = milp(-1)
    assert res.status == 3
    assert not res.success
    msg = "The problem is unbounded. (HiGHS Status 10:"
    assert res.message.startswith(msg)
    assert (res.fun is res.mip_dual_bound is res.mip_gap
            is res.mip_node_count is res.x is None)

