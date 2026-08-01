
def test_validate_bool_kwarg(name, value):
    assert validate_bool_kwarg(value, name) == value

