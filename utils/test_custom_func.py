
def test_custom_func():
    assert m.custom_function(4) == 36
    assert m.roundtrip(m.custom_function)(4) == 36

