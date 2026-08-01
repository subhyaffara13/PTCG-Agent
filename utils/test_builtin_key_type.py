
def test_builtin_key_type():
    """Test that all the keys in the builtin modules have type str.

    Previous versions of pybind11 would add a unicode key in python 2.
    """
    assert all(type(k) == str for k in dir(builtins))

