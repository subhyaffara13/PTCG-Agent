
def test_agg_text_clip():
    np.random.seed(1)
    fig, (ax1, ax2) = plt.subplots(2)
    for x, y in np.random.rand(10, 2):
        ax1.text(x, y, "foo", clip_on=True)
        ax2.text(x, y, "foo")

