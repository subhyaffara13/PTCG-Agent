
def test_latex_pkg_already_loaded(preamble):
    plt.rcParams["text.latex.preamble"] = preamble
    fig = plt.figure()
    fig.text(.5, .5, "hello, world", usetex=True)
    fig.canvas.draw()

