
def test_alive_gc_multi_derived(capture):
    class Derived(m.Parent, m.Child):
        def __init__(self):
            m.Parent.__init__(self)
            m.Child.__init__(self)

    n_inst = ConstructorStats.detail_reg_inst()
    p = Derived()
    p.addChildKeepAlive(m.Child())
    # +3 rather than +2 because Derived corresponds to two registered instances
    assert ConstructorStats.detail_reg_inst() == n_inst + 3
    lst = [p]
    lst.append(lst)  # creates a circular reference
    with capture:
        del p, lst
        assert ConstructorStats.detail_reg_inst() == n_inst
    assert (
        capture
        == """
        Releasing parent.
        Releasing child.
        Releasing child.
    """
    )

