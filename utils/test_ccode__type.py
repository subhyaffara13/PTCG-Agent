
def test_ccode_Type():
    assert ccode(Type('float')) == 'float'
    assert ccode(intc) == 'int'

