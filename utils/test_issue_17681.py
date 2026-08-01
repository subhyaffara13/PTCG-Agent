
def test_issue_17681():
    class identity_func(Function):

        def _eval_evalf(self, *args, **kwargs):
            return self.args[0].evalf(*args, **kwargs)

    assert floor(identity_func(S(0))) == 0
    assert get_integer_part(S(0), 1, {}, True) == (0, 0)

