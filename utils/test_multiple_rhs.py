import random

def test_multiple_rhs():
    random = np.random.RandomState(1234)
    c = random.randn(4)
    r = random.randn(4)
    for offset in [0, 1j]:
        for yshape in ((4,), (4, 3)):
            y = random.randn(*yshape) + offset
            actual = solve_toeplitz((c,r), b=y)
            desired = solve(toeplitz(c, r=r), y)
            assert_equal(actual.shape, yshape)
            assert_equal(desired.shape, yshape)
            assert_allclose(actual, desired)

