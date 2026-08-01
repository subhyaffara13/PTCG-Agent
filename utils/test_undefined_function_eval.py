
def test_undefined_function_eval():
    # Issue 15170. Make sure UndefinedFunction with eval defined works
    # properly.

    fdiff = lambda self, argindex=1: cos(self.args[argindex - 1])
    eval = classmethod(lambda cls, t: None)
    _imp_ = classmethod(lambda cls, t: sin(t))

    temp = Function('temp', fdiff=fdiff, eval=eval, _imp_=_imp_)

    expr = temp(t)
    assert sympify(expr) == expr
    assert type(sympify(expr)).fdiff.__name__ == "<lambda>"
    assert expr.diff(t) == cos(t)

