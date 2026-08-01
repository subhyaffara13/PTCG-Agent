
def test_text_as_text_opacity():
    mpl.rcParams['svg.fonttype'] = 'none'
    plt.figure()
    plt.gca().set_axis_off()
    plt.text(0.25, 0.25, '50% using `color`', color=(0, 0, 0, 0.5))
    plt.text(0.25, 0.5, '50% using `alpha`', alpha=0.5)
    plt.text(0.25, 0.75, '50% using `alpha` and 100% `color`', alpha=0.5,
             color=(0, 0, 0, 1))

