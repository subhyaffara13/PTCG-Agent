
def test_eigen_keepalive():
    a = m.ReturnTester()
    cstats = ConstructorStats.get(m.ReturnTester)
    assert cstats.alive() == 1
    unsafe = [a.ref(), a.ref_const(), a.block(1, 2, 3, 4)]
    copies = [
        a.copy_get(),
        a.copy_view(),
        a.copy_ref(),
        a.copy_ref_const(),
        a.copy_block(4, 3, 2, 1),
    ]
    del a
    assert cstats.alive() == 0
    del unsafe
    del copies

    for meth in [
        m.ReturnTester.get,
        m.ReturnTester.get_ptr,
        m.ReturnTester.view,
        m.ReturnTester.view_ptr,
        m.ReturnTester.ref_safe,
        m.ReturnTester.ref_const_safe,
        m.ReturnTester.corners,
        m.ReturnTester.corners_const,
    ]:
        assert_keeps_alive(m.ReturnTester, meth)

    for meth in [m.ReturnTester.block_safe, m.ReturnTester.block_const]:
        assert_keeps_alive(m.ReturnTester, meth, 4, 3, 2, 1)

