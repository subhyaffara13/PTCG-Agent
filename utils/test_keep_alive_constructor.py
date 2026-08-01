
def test_keep_alive_constructor(capture):
    n_inst = ConstructorStats.detail_reg_inst()

    with capture:
        p = m.Parent(m.Child())
        assert ConstructorStats.detail_reg_inst() == n_inst + 2
    assert (
        capture
        == """
        Allocating child.
        Allocating parent.
    """
    )
    with capture:
        del p
        assert ConstructorStats.detail_reg_inst() == n_inst
    assert (
        capture
        == """
        Releasing parent.
        Releasing child.
    """
    )

