
def test_alive_gc_derived(capture):
    class Derived(m.Parent):
        pass

    n_inst = ConstructorStats.detail_reg_inst()
    p = Derived()
    p.addChildKeepAlive(m.Child())
    assert ConstructorStats.detail_reg_inst() == n_inst + 2
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
    """
    )

