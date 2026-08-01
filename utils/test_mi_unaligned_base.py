
def test_mi_unaligned_base():
    """Returning an offset (non-first MI) base class pointer should recognize the instance"""

    n_inst = ConstructorStats.detail_reg_inst()

    c = m.I801C()
    d = m.I801D()
    # + 4 below because we have the two instances, and each instance has offset base I801B2
    assert ConstructorStats.detail_reg_inst() == n_inst + 4
    b1c = m.i801b1_c(c)
    assert b1c is c
    b2c = m.i801b2_c(c)
    assert b2c is c
    b1d = m.i801b1_d(d)
    assert b1d is d
    b2d = m.i801b2_d(d)
    assert b2d is d

    assert ConstructorStats.detail_reg_inst() == n_inst + 4  # no extra instances
    del c, b1c, b2c
    assert ConstructorStats.detail_reg_inst() == n_inst + 2
    del d, b1d, b2d
    assert ConstructorStats.detail_reg_inst() == n_inst

