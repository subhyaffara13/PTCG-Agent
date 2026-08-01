
def test_move_and_copy_loads():
    """Call some functions that load arguments via custom type casters and count the number of
    moves/copies."""

    cstats = m.move_and_copy_cstats()
    c_m, c_mc, c_c = (
        cstats["MoveOnlyInt"],
        cstats["MoveOrCopyInt"],
        cstats["CopyOnlyInt"],
    )

    assert m.move_only(10) == 10  # 1 move, c_m
    assert m.move_or_copy(11) == 11  # 1 move, c_mc
    assert m.copy_only(12) == 12  # 1 copy, c_c
    assert m.move_pair((13, 14)) == 27  # 1 c_m move, 1 c_mc move
    assert m.move_tuple((15, 16, 17)) == 48  # 2 c_m moves, 1 c_mc move
    assert m.copy_tuple((18, 19)) == 37  # 2 c_c copies
    # Direct constructions: 2 c_m moves, 2 c_mc moves, 1 c_c copy
    # Extra moves/copies when moving pairs/tuples: 3 c_m, 3 c_mc, 2 c_c
    assert m.move_copy_nested((1, ((2, 3, (4,)), 5))) == 15

    assert c_m.copy_assignments + c_m.copy_constructions == 0
    assert c_m.move_assignments == 6
    assert c_m.move_constructions == 9
    assert c_mc.copy_assignments + c_mc.copy_constructions == 0
    assert c_mc.move_assignments == 5
    assert c_mc.move_constructions == 8
    assert c_c.copy_assignments == 4
    assert c_c.copy_constructions == 6
    assert c_m.alive() + c_mc.alive() + c_c.alive() == 0

