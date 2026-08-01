
def test_gettightbbox_ignore_nan():
    fig, ax = plt.subplots()
    remove_ticks_and_titles(fig)
    ax.text(np.nan, 1, 'Boo')
    renderer = fig.canvas.get_renderer()
    np.testing.assert_allclose(ax.get_tightbbox(renderer).width, 496)

