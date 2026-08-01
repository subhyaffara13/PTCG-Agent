
def test_IntBaseType():
    assert intc.name == String('intc')
    assert intc.args == (intc.name,)
    assert str(IntBaseType('a').name) == 'a'

