
def test_markevery_figure_line_unsupported_relsize():
    fig = plt.figure()
    fig.add_artist(mlines.Line2D([0, 1], [0, 1], marker="o", markevery=.5))
    with pytest.raises(ValueError):
        fig.canvas.draw()

