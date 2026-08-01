
def test_xelatex():
    rc_xelatex = {'font.family': 'serif',
                  'pgf.rcfonts': False}
    mpl.rcParams.update(rc_xelatex)
    create_figure()

