
def test_asymmetric_fail(problem_func):
    """Asymmetric matrix should raise `ValueError` when check=True"""
    A, b = problem_func()
    A[1, 2] = 1
    A[2, 1] = 2
    with assert_raises(ValueError):
        xp, info = minres(A, b, check=True)

