
def _assert_unable_to_find_basic_feasible_sol(res):
    # res: linprog result object

    # The status may be either 2 or 4 depending on why the feasible solution
    # could not be found. If the underlying problem is expected to not have a
    # feasible solution, _assert_infeasible should be used.
    assert_(not res.success, "incorrectly reported success")
    assert_(res.status in (2, 4), "failed to report optimization failure")

