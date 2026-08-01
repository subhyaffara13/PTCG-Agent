
def test_mathtext_rendering_lightweight(baseline_images, fontset, index, text):
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.5, 0.5, text, fontsize=12, math_fontfamily=fontset,
             horizontalalignment='center', verticalalignment='center')

