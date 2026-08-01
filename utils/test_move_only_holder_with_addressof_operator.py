
def test_move_only_holder_with_addressof_operator():
    a = m.TypeForMoveOnlyHolderWithAddressOf.make()
    a.print_object()

    stats = ConstructorStats.get(m.TypeForMoveOnlyHolderWithAddressOf)
    assert stats.alive() == 1

    a.value = 42
    assert a.value == 42

    del a
    assert stats.alive() == 0

