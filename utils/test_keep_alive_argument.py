
def test_keep_alive_argument(capture):
    n_inst = ConstructorStats.detail_reg_inst()
    with capture:
        p = m.Parent()
    assert capture == "Allocating parent."
    with capture:
        p.addChild(m.Child())
        assert ConstructorStats.detail_reg_inst() == n_inst + 1
    assert (
        capture
        == """
        Allocating child.
        Releasing child.
    """
    )
    with capture:
        del p
        assert ConstructorStats.detail_reg_inst() == n_inst
    assert capture == "Releasing parent."

    with capture:
        p = m.Parent()
    assert capture == "Allocating parent."
    with capture:
        p.addChildKeepAlive(m.Child())
        assert ConstructorStats.detail_reg_inst() == n_inst + 2
    assert capture == "Allocating child."
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

    p = m.Parent()
    c = m.Child()
    assert ConstructorStats.detail_reg_inst() == n_inst + 2
    m.free_function(p, c)
    del c
    assert ConstructorStats.detail_reg_inst() == n_inst + 2
    del p
    assert ConstructorStats.detail_reg_inst() == n_inst

    with pytest.raises(RuntimeError) as excinfo:
        m.invalid_arg_index()
    assert str(excinfo.value) == "Could not activate keep_alive!"

