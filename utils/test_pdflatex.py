
def test_pdflatex():
    rc_pdflatex = {'font.family': 'serif',
                   'pgf.rcfonts': False,
                   'pgf.texsystem': 'pdflatex',
                   'pgf.preamble': ('\\usepackage[utf8x]{inputenc}'
                                    '\\usepackage[T1]{fontenc}')}
    mpl.rcParams.update(rc_pdflatex)
    create_figure()

