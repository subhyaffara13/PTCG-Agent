
def test_extensibility_eval():
    class MyFunc(Function):
        @classmethod
        def eval(cls, *args):
            return (0, 0, 0)
    assert MyFunc(0) == (0, 0, 0)

