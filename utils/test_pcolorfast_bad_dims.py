
def test_pcolorfast_bad_dims():
    fig, ax = plt.subplots()
    with pytest.raises(
            TypeError, match=("the given X was 1D and the given Y was 2D")):
        ax.pcolorfast(np.empty(6), np.empty((4, 7)), np.empty((8, 8)))

