
def test_string_with_unit(constructor, value, unit):
    with pytest.raises(ValueError, match="unit must not be specified"):
        constructor(value, unit=unit)

