
def test_invalid_field_name_warning():
    names_vars = (
        ('_1', mlarr(np.arange(10))),
        ('mystr', mlarr('a string')))
    check_mat_write_warning(names_vars)

    names_vars = (('mymap', {"a": 1, "_b": 2}),)
    check_mat_write_warning(names_vars)

    names_vars = (('mymap', {"a": 1, "1a": 2}),)
    check_mat_write_warning(names_vars)

