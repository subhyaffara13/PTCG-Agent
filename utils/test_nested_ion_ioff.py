
def test_nested_ion_ioff():
    # initial state is interactive
    plt.ion()

    # mixed ioff/ion
    with plt.ioff():
        assert not mpl.is_interactive()
        with plt.ion():
            assert mpl.is_interactive()
        assert not mpl.is_interactive()
    assert mpl.is_interactive()

    # redundant contexts
    with plt.ioff():
        with plt.ioff():
            assert not mpl.is_interactive()
    assert mpl.is_interactive()

    with plt.ion():
        plt.ioff()
    assert mpl.is_interactive()

    # initial state is not interactive
    plt.ioff()

    # mixed ioff/ion
    with plt.ion():
        assert mpl.is_interactive()
        with plt.ioff():
            assert not mpl.is_interactive()
        assert mpl.is_interactive()
    assert not mpl.is_interactive()

    # redundant contexts
    with plt.ion():
        with plt.ion():
            assert mpl.is_interactive()
    assert not mpl.is_interactive()

    with plt.ioff():
        plt.ion()
    assert not mpl.is_interactive()

