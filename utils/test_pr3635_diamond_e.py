
def test_pr3635_diamond_e():
    o = m.MVE()
    assert o.b == 1
    assert o.c == 2
    assert o.d0 == 3
    assert o.d1 == 4
    assert o.e == 5

    assert o.get_b_b() == 1
    assert o.get_c_b() == 1
    assert o.get_d0_b() == 1
    assert o.get_d1_b() == 1
    assert o.get_e_b() == 1

    assert o.get_c_c() == 2
    assert o.get_d0_c() == 2
    assert o.get_d1_c() == 2
    assert o.get_e_c() == 2

    assert o.get_d0_d0() == 3
    assert o.get_e_d0() == 3

    assert o.get_d1_d1() == 4
    assert o.get_e_d1() == 4

    assert o.get_e_e() == 5

