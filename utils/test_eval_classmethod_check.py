
def test_eval_classmethod_check():
    with raises(TypeError):
        class F(Function):
            def eval(self, x):
                pass

