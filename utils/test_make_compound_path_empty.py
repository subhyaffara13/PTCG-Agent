
def test_make_compound_path_empty():
    # We should be able to make a compound path with no arguments.
    # This makes it easier to write generic path based code.
    empty = Path.make_compound_path()
    assert empty.vertices.shape == (0, 2)
    r2 = Path.make_compound_path(empty, empty)
    assert r2.vertices.shape == (0, 2)
    assert r2.codes.shape == (0,)
    r3 = Path.make_compound_path(Path([(0, 0)]), empty)
    assert r3.vertices.shape == (1, 2)
    assert r3.codes.shape == (1,)

