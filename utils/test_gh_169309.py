import math


def test_gh_169309():
    x = np.repeat(10, 9)
    actual = scipy.linalg.blas.dnrm2(x, 5, 3, -1)
    expected = math.sqrt(500)
    assert_allclose(actual, expected)

