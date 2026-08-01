
def test_ion():
    plt.ioff()
    assert not mpl.is_interactive()
    with plt.ion():
        assert mpl.is_interactive()
    assert not mpl.is_interactive()

    plt.ion()
    assert mpl.is_interactive()
    with plt.ion():
        assert mpl.is_interactive()
    assert mpl.is_interactive()

