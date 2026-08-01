
def test_issue_3531b():
    class Foo:
        def __init__(self):
            self.field = 1.0

        def __mul__(self, other):
            self.field = self.field * other

        def __rmul__(self, other):
            self.field = other * self.field
    f = Foo()
    x = Symbol("x")
    assert f*x == x*f

