
def test_no_integration():
    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        sol = solve_ivp(lambda t, y: -y, [4, 4], [2, 3],
                        method=method, dense_output=True)
        assert_equal(sol.sol(4), [2, 3])
        assert_equal(sol.sol([4, 5, 6]), [[2, 2, 2], [3, 3, 3]])

