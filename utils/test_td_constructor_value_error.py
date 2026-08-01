
def test_td_constructor_value_error():
    msg = "Invalid type <class 'str'>. Must be int or float."
    with pytest.raises(TypeError, match=msg):
        Timedelta(nanoseconds="abc")

