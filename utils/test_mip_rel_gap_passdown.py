
def test_mip_rel_gap_passdown():
    # Solve problem with decreasing mip_gap to make sure mip_rel_gap decreases
    # Adapted from test_linprog::TestLinprogHiGHSMIP::test_mip_rel_gap_passdown
    # MIP taken from test_mip_6 above
    A_eq = np.array([[22, 13, 26, 33, 21, 3, 14, 26],
                     [39, 16, 22, 28, 26, 30, 23, 24],
                     [18, 14, 29, 27, 30, 38, 26, 26],
                     [41, 26, 28, 36, 18, 38, 16, 26]])
    b_eq = np.array([7872, 10466, 11322, 12058])
    c = np.array([2, 10, 13, 17, 7, 5, 7, 3])

    mip_rel_gaps = [0.25, 0.01, 0.001]
    sol_mip_gaps = []
    for mip_rel_gap in mip_rel_gaps:
        res = milp(c=c, bounds=(0, np.inf), constraints=(A_eq, b_eq, b_eq),
                   integrality=True, options={"mip_rel_gap": mip_rel_gap})
        # assert that the solution actually has mip_gap lower than the
        # required mip_rel_gap supplied
        assert res.mip_gap <= mip_rel_gap
        # check that `res.mip_gap` is as defined in the documentation
        assert res.mip_gap == (res.fun - res.mip_dual_bound)/res.fun
        sol_mip_gaps.append(res.mip_gap)

    # make sure that the mip_rel_gap parameter is actually doing something
    # check that differences between solution gaps are declining
    # monotonically with the mip_rel_gap parameter.
    assert np.all(np.diff(sol_mip_gaps) < 0)

