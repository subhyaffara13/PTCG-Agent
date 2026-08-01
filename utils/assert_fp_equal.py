
def assert_fp_equal(x, y, err_msg="", nulp=50):
    """Assert two arrays are equal, up to some floating-point rounding error"""
    try:
        assert_array_almost_equal_nulp(x, y, nulp)
    except AssertionError as e:
        raise AssertionError(f"{e}\n{err_msg}") from e


def assert_fp_equal(a, b):
    assert (np.abs(a - b) < 1e-12).all()

