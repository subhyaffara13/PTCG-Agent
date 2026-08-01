
def test_conditionally_positive_definite(kernel):
    # Test if each kernel in _AVAILABLE is conditionally positive definite of
    # order m, where m comes from _NAME_TO_MIN_DEGREE. This is a necessary
    # condition for the smoothed RBF interpolant to be well-posed in general.
    m = _NAME_TO_MIN_DEGREE.get(kernel, -1) + 1
    assert _is_conditionally_positive_definite(kernel, m)

