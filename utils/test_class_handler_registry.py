
def test_class_handler_registry():
    my_handler_registry = ClassFactRegistry()

    # The predicate doesn't matter here, so just pass
    @my_handler_registry.register(Mul)
    def fact1(expr):
        pass
    @my_handler_registry.multiregister(Expr)
    def fact2(expr):
        pass

    assert my_handler_registry[Basic] == (frozenset(), frozenset())
    assert my_handler_registry[Expr] == (frozenset(), frozenset({fact2}))
    assert my_handler_registry[Mul] == (frozenset({fact1}), frozenset({fact2}))

