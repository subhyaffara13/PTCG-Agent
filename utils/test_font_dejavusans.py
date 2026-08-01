
def test_font_dejavusans():
    # DejaVuSans uses the seac operator to compose characters with diacritics
    mpl.rcParams['text.latex.preamble'] = '\n'.join((
        r'\usepackage{DejaVuSans}',
        r'\usepackage[T1]{fontenc}',
        r'\usepackage[utf8]{inputenc}'
    ))

    fig, ax = plt.subplots()
    ax.text(0.1, 0.1, r"\textsf{ñäö ABCDabcd}", usetex=True, fontsize=50)
    ax.text(0.1, 0.3, r"\textsf{fi ffl 1234}", usetex=True, fontsize=50)
    ax.set_xticks([])
    ax.set_yticks([])

