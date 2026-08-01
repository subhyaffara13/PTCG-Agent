
def test_predicates():
    predicates = [
        getattr(Q, attr)
        for attr in Q.__class__.__dict__
        if not attr.startswith('__')]
    for p in predicates:
        assert _test_args(p)

