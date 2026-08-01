
def _assert_iteration_limit_reached(res, maxiter):
    assert_(not res.success, "Incorrectly reported success")
    assert_(res.success < maxiter, "Incorrectly reported number of iterations")
    assert_equal(res.status, 1, "Failed to report iteration limit reached")

