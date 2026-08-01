
def test_ioff():
    plt.ion()
    assert mpl.is_interactive()
    with plt.ioff():
        assert not mpl.is_interactive()
    assert mpl.is_interactive()

    plt.ioff()
    assert not mpl.is_interactive()
    with plt.ioff():
        assert not mpl.is_interactive()
    assert not mpl.is_interactive()

