
def test_pr3635_diamond_d1():
    o = m.MVD1()
    assert o.b == 1
    assert o.c == 2
    assert o.d1 == 4

    assert o.get_b_b() == 1
    assert o.get_c_b() == 1
    assert o.get_d1_b() == 1

    assert o.get_c_c() == 2
    assert o.get_d1_c() == 2

    assert o.get_d1_d1() == 4

