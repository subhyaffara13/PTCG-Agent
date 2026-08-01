
def test_longdouble_from_bool(bool_val):
    assert np.longdouble(bool_val) == np.longdouble(int(bool_val))

