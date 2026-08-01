
def test_subfigure_dpi():
    fig = plt.figure(dpi=100)
    sub_fig = fig.subfigures()
    assert sub_fig.get_dpi() == fig.get_dpi()

    sub_fig.set_dpi(200)
    assert sub_fig.get_dpi() == 200
    assert fig.get_dpi() == 200

