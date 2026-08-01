
def test_issue_7688():
    from sympy.core.function import Function, UndefinedFunction

    f = Function('f')  # actually an UndefinedFunction
    clear_cache()
    class A(UndefinedFunction):
        pass
    a = A('f')
    assert isinstance(a, type(f))

