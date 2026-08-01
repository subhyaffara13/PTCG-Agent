
def test_no_pyplot():
    # tests pickle-ability of a figure not created with pyplot
    from matplotlib.backends.backend_pdf import FigureCanvasPdf
    fig = mfigure.Figure()
    _ = FigureCanvasPdf(fig)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot([1, 2, 3], [1, 2, 3])
    pickle.dump(fig, BytesIO(), pickle.HIGHEST_PROTOCOL)

