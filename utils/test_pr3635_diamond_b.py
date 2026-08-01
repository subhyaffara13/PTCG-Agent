
def test_pr3635_diamond_b():
    o = m.MVB()
    assert o.b == 1

    assert o.get_b_b() == 1

