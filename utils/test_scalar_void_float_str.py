
def test_scalar_void_float_str():
    # Note that based on this currently we do not print the same as a tuple
    # would, since the tuple would include the repr() inside for floats, but
    # we do not do that.
    scalar = np.void((1.0, 2.0), dtype=[('f0', '<f8'), ('f1', '>f4')])
    assert str(scalar) == "(1.0, 2.0)"

