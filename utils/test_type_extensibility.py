
def test_type_extensibility():
    """test that new types can be added to the ask system at runtime
    """
    from sympy.core import Basic

    class MyType(Basic):
        pass

    @Q.prime.register(MyType)
    def _(expr, assumptions):
        return True

    assert ask(Q.prime(MyType())) is True

