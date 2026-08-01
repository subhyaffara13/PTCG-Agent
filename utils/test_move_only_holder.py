
def test_move_only_holder():
    a = m.TypeWithMoveOnlyHolder.make()
    b = m.TypeWithMoveOnlyHolder.make_as_object()
    stats = ConstructorStats.get(m.TypeWithMoveOnlyHolder)
    assert stats.alive() == 2
    del b
    assert stats.alive() == 1
    del a
    assert stats.alive() == 0

