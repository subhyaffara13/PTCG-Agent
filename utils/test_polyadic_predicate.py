
def test_polyadic_predicate():

    class SexyPredicate(Predicate):
        pass
    try:
        Q.sexyprime = SexyPredicate()

        @Q.sexyprime.register(Integer, Integer)
        def _(int1, int2, assumptions):
            args = sorted([int1, int2])
            if not all(ask(Q.prime(a), assumptions) for a in args):
                return False
            return args[1] - args[0] == 6

        @Q.sexyprime.register(Integer, Integer, Integer)
        def _(int1, int2, int3, assumptions):
            args = sorted([int1, int2, int3])
            if not all(ask(Q.prime(a), assumptions) for a in args):
                return False
            return args[2] - args[1] == 6 and args[1] - args[0] == 6

        assert ask(Q.sexyprime(5, 11))
        assert ask(Q.sexyprime(7, 13, 19))
    finally:
        del Q.sexyprime

