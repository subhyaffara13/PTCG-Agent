
def test_badsubplotgrid():
    # test that we get warning for mismatched subplot grids, not than an error
    plt.subplot2grid((4, 5), (0, 0))
    # this is the bad entry:
    plt.subplot2grid((5, 5), (0, 3), colspan=3, rowspan=5)
    with pytest.warns(UserWarning):
        plt.tight_layout()

