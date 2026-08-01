
def fake_to_terminal():
    yield ('a', ('mystr',), {'error': True})
    yield ('b', (), {})
    yield (('p1', 'p2'), (), {'indent': 1})

