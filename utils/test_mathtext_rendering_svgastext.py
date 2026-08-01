
def test_mathtext_rendering_svgastext(baseline_images, fontset, index, text):
    mpl.rcParams['mathtext.fontset'] = fontset
    mpl.rcParams['svg.fonttype'] = 'none'  # Minimize image size.
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.patch.set(visible=False)  # Minimize image size.
    fig.text(0.5, 0.5, text, fontsize=16,
             horizontalalignment='center', verticalalignment='center')

