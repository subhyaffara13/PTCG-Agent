
def test_unknown_solvers_and_options():
    c = np.array([-3, -2])
    A_ub = [[2, 1], [1, 1], [1, 0]]
    b_ub = [10, 8, 4]

    assert_raises(ValueError, linprog,
                  c, A_ub=A_ub, b_ub=b_ub, method='ekki-ekki-ekki')
    assert_raises(ValueError, linprog,
                  c, A_ub=A_ub, b_ub=b_ub, method='highs-ekki')
    message = "Unrecognized options detected: {'rr_method': 'ekki-ekki-ekki'}"
    with pytest.warns(OptimizeWarning, match=message):
        linprog(c, A_ub=A_ub, b_ub=b_ub,
                options={"rr_method": 'ekki-ekki-ekki'})

