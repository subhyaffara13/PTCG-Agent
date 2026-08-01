
def test_mathtext_rendering(baseline_images, fontset, index, text):
    mpl.rcParams['mathtext.fontset'] = fontset
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.5, 0.5, text, fontsize=12,
             horizontalalignment='center', verticalalignment='center')

