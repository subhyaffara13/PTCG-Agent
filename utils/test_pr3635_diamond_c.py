
def test_pr3635_diamond_c():
    o = m.MVC()
    assert o.b == 1
    assert o.c == 2

    assert o.get_b_b() == 1
    assert o.get_c_b() == 1

    assert o.get_c_c() == 2

