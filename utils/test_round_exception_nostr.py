
def test_round_exception_nostr():
    # Don't use the string form of the expression in the round exception, as
    # it's too slow
    s = Symbol('bad')
    try:
        s.round()
    except TypeError as e:
        assert 'bad' not in str(e)
    else:
        # Did not raise
        raise AssertionError("Did not raise")

