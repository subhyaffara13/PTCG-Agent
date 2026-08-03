import random

def test_zero_diag_error():
    # The Levinson-Durbin implementation fails when the diagonal is zero.
    random = np.random.RandomState(1234)
    n = 4
    c = random.randn(n)
    r = random.randn(n)
    y = random.randn(n)
    c[0] = 0
    assert_raises(np.linalg.LinAlgError,
        solve_toeplitz, (c, r), b=y)

