
def test_font_heuristica():
    # Heuristica uses the callothersubr operator for some glyphs
    mpl.rcParams['text.latex.preamble'] = '\n'.join((
        r'\usepackage{heuristica}',
        r'\usepackage[T1]{fontenc}',
        r'\usepackage[utf8]{inputenc}'
    ))
    fig, ax = plt.subplots()
    ax.text(0.1, 0.1, r"BHTem fi ffl 1234", usetex=True, fontsize=50)
    ax.set_xticks([])
    ax.set_yticks([])

