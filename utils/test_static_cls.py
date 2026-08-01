
def test_static_cls():
    """Static property getter and setters expect the type object as the their only argument"""

    instance = m.TestProperties()
    assert m.TestProperties.static_cls is m.TestProperties
    assert instance.static_cls is m.TestProperties

    def check_self(self):
        assert self is m.TestProperties

    m.TestProperties.static_cls = check_self
    instance.static_cls = check_self

