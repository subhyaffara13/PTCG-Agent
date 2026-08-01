
def test_power_dispatcher():

    class NewBase(Expr):
        pass
    class NewPow(NewBase, Pow):
        pass
    a, b = Symbol('a'), NewBase()

    @power.register(Expr, NewBase)
    @power.register(NewBase, Expr)
    @power.register(NewBase, NewBase)
    def _(a, b):
        return NewPow(a, b)

    # Pow called as fallback
    assert power(2, 3) == 8*S.One
    assert power(a, 2) == Pow(a, 2)
    assert power(a, a) == Pow(a, a)

    # NewPow called by dispatch
    assert power(a, b) == NewPow(a, b)
    assert power(b, a) == NewPow(b, a)
    assert power(b, b) == NewPow(b, b)

