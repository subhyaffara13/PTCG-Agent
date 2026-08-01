
def test_key_extensibility():
    """test that you can add keys to the ask system at runtime"""
    # make sure the key is not defined
    raises(AttributeError, lambda: ask(Q.my_key(x)))

    # Old handler system
    class MyAskHandler(AskHandler):
        @staticmethod
        def Symbol(expr, assumptions):
            return True
    try:
        with warns_deprecated_sympy():
            register_handler('my_key', MyAskHandler)
        with warns_deprecated_sympy():
            assert ask(Q.my_key(x)) is True
        with warns_deprecated_sympy():
            assert ask(Q.my_key(x + 1)) is None
    finally:
        # We have to disable the stacklevel testing here because this raises
        # the warning twice from two different places
        with warns_deprecated_sympy():
            remove_handler('my_key', MyAskHandler)
        del Q.my_key
    raises(AttributeError, lambda: ask(Q.my_key(x)))

    # New handler system
    class MyPredicate(Predicate):
        pass
    try:
        Q.my_key = MyPredicate()
        @Q.my_key.register(Symbol)
        def _(expr, assumptions):
            return True
        assert ask(Q.my_key(x)) is True
        assert ask(Q.my_key(x+1)) is None
    finally:
        del Q.my_key
    raises(AttributeError, lambda: ask(Q.my_key(x)))

