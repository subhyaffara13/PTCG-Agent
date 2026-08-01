
def test_figure_label_replaced():
    plt.close('all')
    fig = plt.figure(1)
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match="Changing 'Figure.number' is deprecated"):
        fig.number = 2
    assert fig.number == 2

