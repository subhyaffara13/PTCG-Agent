
def test_truetype_conversion(recwarn):
    mpl.rcParams['pdf.fonttype'] = 3
    fig, ax = plt.subplots()
    ax.text(0, 0, "ABCDE",
            font=Path(__file__).parent / "data/mpltest.ttf", fontsize=72)
    ax.set_xticks([])
    ax.set_yticks([])

