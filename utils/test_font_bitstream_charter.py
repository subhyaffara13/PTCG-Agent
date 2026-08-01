
def test_font_bitstream_charter():
    mpl.rcParams['text.latex.preamble'] = '\n'.join((
        r'\usepackage{charter}',
        r'\usepackage[T1]{fontenc}',
        r'\usepackage[utf8]{inputenc}'
    ))
    fig, ax = plt.subplots()
    ax.text(0.1, 0.1, r"åüš ABCDabcd", usetex=True, fontsize=50)
    ax.text(0.1, 0.3, r"fi ffl 1234", usetex=True, fontsize=50)
    ax.set_xticks([])
    ax.set_yticks([])

