
def test_mul_dispatcher():

    class NewBase(Expr):
        @property
        def _mul_handler(self):
            return NewMul
    class NewMul(NewBase, Mul):
        pass
    mul.register_handlerclass((Mul, NewMul), NewMul)

    a, b = Symbol('a'), NewBase()

    # Mul called as fallback
    assert mul(1, 2) == Mul(1, 2)
    assert mul(a, a) == Mul(a, a)

    # selection by registered priority
    assert mul(a,b,a) == NewMul(a**2, b)

