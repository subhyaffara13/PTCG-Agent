
def test_is_setter():
    fld = m.exercise_is_setter.Field()
    assert fld.int_value == -99
    setter_return = fld.int_value = 100
    assert isinstance(setter_return, int)
    assert setter_return == 100
    assert fld.int_value == 100

