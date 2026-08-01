
def test_usetex_packages(pkg):
    if not _has_tex_package(pkg):
        pytest.skip(f'{pkg} is not available')
    mpl.rcParams['text.usetex'] = True

    fig = plt.figure()
    text = fig.text(0.5, 0.5, "Some text 0123456789")
    fig.canvas.draw()

    mpl.rcParams['text.latex.preamble'] = (
        r'\PassOptionsToPackage{dvipsnames}{xcolor}\usepackage{%s}' % pkg)
    fig = plt.figure()
    text2 = fig.text(0.5, 0.5, "Some text 0123456789")
    fig.canvas.draw()
    np.testing.assert_array_equal(text2.get_window_extent(),
                                  text.get_window_extent())

