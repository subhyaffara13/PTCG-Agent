
def test_figure_no_label():
    # standalone figures do not have a figure attribute
    fig = Figure()
    with pytest.raises(AttributeError):
        fig.number
    # but one can set one
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match="Changing 'Figure.number' is deprecated"):
        fig.number = 5
    assert fig.number == 5
    # even though it's not known by pyplot
    assert not plt.fignum_exists(fig.number)

