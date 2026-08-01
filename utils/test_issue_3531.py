
def test_issue_3531():
    # https://github.com/sympy/sympy/issues/3531
    # https://github.com/sympy/sympy/pull/18116
    class MightyNumeric(tuple):
        __slots__ = ()

        def __rtruediv__(self, other):
            return "something"

    assert sympify(1)/MightyNumeric((1, 2)) == "something"

