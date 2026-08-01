
def test_pr3635_diamond_d0():
    o = m.MVD0()
    assert o.b == 1
    assert o.c == 2
    assert o.d0 == 3

    assert o.get_b_b() == 1
    assert o.get_c_b() == 1
    assert o.get_d0_b() == 1

    assert o.get_c_c() == 2
    assert o.get_d0_c() == 2

    assert o.get_d0_d0() == 3

