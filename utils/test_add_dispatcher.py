
def test_add_dispatcher():

    class NewBase(Expr):
        @property
        def _add_handler(self):
            return NewAdd
    class NewAdd(NewBase, Add):
        pass
    add.register_handlerclass((Add, NewAdd), NewAdd)

    a, b = Symbol('a'), NewBase()

    # Add called as fallback
    assert add(1, 2) == Add(1, 2)
    assert add(a, a) == Add(a, a)

    # selection by registered priority
    assert add(a,b,a) == NewAdd(2*a, b)

