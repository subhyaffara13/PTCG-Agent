
def test_mi_base_return():
    """Tests returning an offset (non-first MI) base class pointer to a derived instance"""

    n_inst = ConstructorStats.detail_reg_inst()

    c1 = m.i801c_b1()
    assert type(c1) is m.I801C
    assert c1.a == 1
    assert c1.b == 2

    d1 = m.i801d_b1()
    assert type(d1) is m.I801D
    assert d1.a == 1
    assert d1.b == 2

    assert ConstructorStats.detail_reg_inst() == n_inst + 4

    c2 = m.i801c_b2()
    assert type(c2) is m.I801C
    assert c2.a == 1
    assert c2.b == 2

    d2 = m.i801d_b2()
    assert type(d2) is m.I801D
    assert d2.a == 1
    assert d2.b == 2

    assert ConstructorStats.detail_reg_inst() == n_inst + 8

    del c2
    assert ConstructorStats.detail_reg_inst() == n_inst + 6
    del c1, d1, d2
    assert ConstructorStats.detail_reg_inst() == n_inst

    # Returning an unregistered derived type with a registered base; we won't
    # pick up the derived type, obviously, but should still work (as an object
    # of whatever type was returned).
    e1 = m.i801e_c()
    assert type(e1) is m.I801C
    assert e1.a == 1
    assert e1.b == 2

    e2 = m.i801e_b2()
    assert type(e2) is m.I801B2
    assert e2.b == 2

