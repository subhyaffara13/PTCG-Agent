
def test_multiple_inheritance_mix1():
    class Base1:
        def __init__(self, i):
            self.i = i

        def foo(self):
            return self.i

    class MITypePy(Base1, m.Base2):
        def __init__(self, i, j):
            Base1.__init__(self, i)
            m.Base2.__init__(self, j)

    mt = MITypePy(3, 4)

    assert mt.foo() == 3
    assert mt.bar() == 4

