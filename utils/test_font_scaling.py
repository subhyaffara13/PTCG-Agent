
def test_font_scaling():
    mpl.rcParams['pdf.fonttype'] = 42
    fig, ax = plt.subplots(figsize=(6.4, 12.4))
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.set_ylim(-10, 600)

    for i, fs in enumerate(range(4, 43, 2)):
        ax.text(0.1, i*30, f"{fs} pt font size", fontsize=fs)

