
def _assert_unbounded(res):
    # res: linprog result object
    assert_(not res.success, "incorrectly reported success")
    assert_equal(res.status, 3, "failed to report unbounded status")

