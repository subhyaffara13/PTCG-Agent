
def test_multiple_inheritance():
    class MITest(m.TestFactory1, m.TestFactory2):
        def __init__(self):
            m.TestFactory1.__init__(self, tag.unique_ptr, 33)
            m.TestFactory2.__init__(self, tag.move)

    a = MITest()
    assert m.TestFactory1.value.fget(a) == "33"
    assert m.TestFactory2.value.fget(a) == "(empty2)"

