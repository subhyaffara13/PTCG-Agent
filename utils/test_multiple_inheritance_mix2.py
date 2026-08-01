
def test_multiple_inheritance_mix2():
    class Base2:
        def __init__(self, i):
            self.i = i

        def bar(self):
            return self.i

    class MITypePy(m.Base1, Base2):
        def __init__(self, i, j):
            m.Base1.__init__(self, i)
            Base2.__init__(self, j)

    mt = MITypePy(3, 4)

    assert mt.foo() == 3
    assert mt.bar() == 4

