
def test_load_template():
    mpl.use("template")
    assert type(plt.figure().canvas) == FigureCanvasTemplate

