
def test_basic5():
    class my(Function):
        @classmethod
        def eval(cls, arg):
            if arg is S.Infinity:
                return S.NaN
    assert limit(my(x), x, oo) == Limit(my(x), x, oo)

