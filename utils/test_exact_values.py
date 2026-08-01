
def test_exact_values():
    # Check that updating stored values with exact ones worked.
    exact = dict((k, v[0]) for k, v in _cd._physical_constants_2018.items())
    replace = _cd.exact2018(exact)
    for key, val in replace.items():
        assert_equal(val, value(key))
        assert precision(key) == 0

