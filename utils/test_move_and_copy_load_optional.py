
def test_move_and_copy_load_optional():
    """Tests move/copy loads of std::optional arguments"""

    cstats = m.move_and_copy_cstats()
    c_m, c_mc, c_c = (
        cstats["MoveOnlyInt"],
        cstats["MoveOrCopyInt"],
        cstats["CopyOnlyInt"],
    )

    # The extra move/copy constructions below come from the std::optional move (which has to move
    # its arguments):
    assert m.move_optional(10) == 10  # c_m: 1 move assign, 2 move construct
    assert m.move_or_copy_optional(11) == 11  # c_mc: 1 move assign, 2 move construct
    assert m.copy_optional(12) == 12  # c_c: 1 copy assign, 2 copy construct
    # 1 move assign + move construct moves each of c_m, c_mc, 1 c_c copy
    # +1 move/copy construct each from moving the tuple
    # +1 move/copy construct each from moving the optional (which moves the tuple again)
    assert m.move_optional_tuple((3, 4, 5)) == 12

    assert c_m.copy_assignments + c_m.copy_constructions == 0
    assert c_m.move_assignments == 2
    assert c_m.move_constructions == 5
    assert c_mc.copy_assignments + c_mc.copy_constructions == 0
    assert c_mc.move_assignments == 2
    assert c_mc.move_constructions == 5
    assert c_c.copy_assignments == 2
    assert c_c.copy_constructions == 5
    assert c_m.alive() + c_mc.alive() + c_c.alive() == 0

