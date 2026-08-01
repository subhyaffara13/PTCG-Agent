
def _assertGradAndGradgradChecks(test_case, apply_fn, inputs, **kwargs):
    # call assert function rather than returning a bool since it's nicer
    # if we get whether this failed on the gradcheck or the gradgradcheck.
    test_case.assertTrue(gradcheck(apply_fn, inputs, **kwargs))
    test_case.assertTrue(gradgradcheck(apply_fn, inputs, **kwargs))

