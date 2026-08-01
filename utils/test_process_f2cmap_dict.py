
def test_process_f2cmap_dict():
    from numpy.f2py.auxfuncs import process_f2cmap_dict

    f2cmap_all = {"integer": {"8": "rubbish_type"}}
    new_map = {"INTEGER": {"4": "int"}}
    c2py_map = {"int": "int", "rubbish_type": "long"}

    exp_map, exp_maptyp = ({"integer": {"8": "rubbish_type", "4": "int"}}, ["int"])

    # Call the function
    res_map, res_maptyp = process_f2cmap_dict(f2cmap_all, new_map, c2py_map)

    # Assert the result is as expected
    assert res_map == exp_map
    assert res_maptyp == exp_maptyp

