
def test_custom_AskHandler():
    from sympy.logic.boolalg import conjuncts

    # Old handler system
    class MersenneHandler(AskHandler):
        @staticmethod
        def Integer(expr, assumptions):
            if ask(Q.integer(log(expr + 1, 2))):
                return True
        @staticmethod
        def Symbol(expr, assumptions):
            if expr in conjuncts(assumptions):
                return True
    try:
        with warns_deprecated_sympy():
            register_handler('mersenne', MersenneHandler)
        n = Symbol('n', integer=True)
        with warns_deprecated_sympy():
            assert ask(Q.mersenne(7))
        with warns_deprecated_sympy():
            assert ask(Q.mersenne(n), Q.mersenne(n))
    finally:
        del Q.mersenne

    # New handler system
    class MersennePredicate(Predicate):
        pass
    try:
        Q.mersenne = MersennePredicate()
        @Q.mersenne.register(Integer)
        def _(expr, assumptions):
            if ask(Q.integer(log(expr + 1, 2))):
                return True
        @Q.mersenne.register(Symbol)
        def _(expr, assumptions):
            if expr in conjuncts(assumptions):
                return True
        assert ask(Q.mersenne(7))
        assert ask(Q.mersenne(n), Q.mersenne(n))
    finally:
        del Q.mersenne

