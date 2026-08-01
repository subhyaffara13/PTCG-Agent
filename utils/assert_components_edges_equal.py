
def assert_components_edges_equal(x, y):
    sx = {frozenset(frozenset(e) for e in c) for c in x}
    sy = {frozenset(frozenset(e) for e in c) for c in y}
    assert sx == sy

