
def _test_stop_on_non_basics(trav):
    def add_one_if_can(expr):
        try:
            return expr + 1
        except TypeError:
            return expr

    expr = Basic(S(1), Str('a'), Basic(S(2), Str('b')))
    expected = Basic(S(2), Str('a'), Basic(S(3), Str('b')))
    rl = trav(add_one_if_can)

    assert rl(expr) == expected

