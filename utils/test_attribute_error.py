
def test_attribute_error():
    raises(AttributeError, lambda: x.cos())
    raises(AttributeError, lambda: x.sin())
    raises(AttributeError, lambda: x.exp())

