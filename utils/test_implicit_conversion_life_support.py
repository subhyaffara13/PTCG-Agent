
def test_implicit_conversion_life_support():
    """Ensure the lifetime of temporary objects created for implicit conversions"""
    assert m.implicitly_convert_argument(UserType(5)) == 5
    assert m.implicitly_convert_variable(UserType(5)) == 5

    assert "outside a bound function" in m.implicitly_convert_variable_fail(UserType(5))

