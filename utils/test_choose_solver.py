
def test_choose_solver():
    # 'highs' chooses 'dual'
    c = np.array([-3, -2])
    A_ub = [[2, 1], [1, 1], [1, 0]]
    b_ub = [10, 8, 4]

    res = linprog(c, A_ub, b_ub, method='highs')
    _assert_success(res, desired_fun=-18.0, desired_x=[2, 6])

