
def assert_quad(value_and_err, tabled_value, error_tolerance=1.5e-8):
    value, err = value_and_err
    assert_allclose(value, tabled_value, atol=err, rtol=0)
    if error_tolerance is not None:
        assert_array_less(err, error_tolerance)

