
def test_eval_sympified():
    # Check both arguments and return types from eval are sympified

    class F(Function):
        @classmethod
        def eval(cls, x):
            assert x is S.One
            return 1

    assert F(1) is S.One

    # String arguments are not allowed
    class F2(Function):
        @classmethod
        def eval(cls, x):
            if x == 0:
                return '1'

    raises(SympifyError, lambda: F2(0))
    F2(1) # Doesn't raise

