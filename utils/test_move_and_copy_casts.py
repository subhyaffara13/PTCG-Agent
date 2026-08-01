
def test_move_and_copy_casts():
    """Cast some values in C++ via custom type casters and count the number of moves/copies."""

    cstats = m.move_and_copy_cstats()
    c_m, c_mc, c_c = (
        cstats["MoveOnlyInt"],
        cstats["MoveOrCopyInt"],
        cstats["CopyOnlyInt"],
    )

    # The type move constructions/assignments below each get incremented: the move assignment comes
    # from the type_caster load; the move construction happens when extracting that via a cast or
    # loading into an argument.
    assert m.move_and_copy_casts(3) == 18
    assert c_m.copy_assignments + c_m.copy_constructions == 0
    assert c_m.move_assignments == 2
    assert c_m.move_constructions >= 2
    assert c_mc.alive() == 0
    assert c_mc.copy_assignments + c_mc.copy_constructions == 0
    assert c_mc.move_assignments == 2
    assert c_mc.move_constructions >= 2
    assert c_c.alive() == 0
    assert c_c.copy_assignments == 2
    assert c_c.copy_constructions >= 2
    assert c_m.alive() + c_mc.alive() + c_c.alive() == 0

