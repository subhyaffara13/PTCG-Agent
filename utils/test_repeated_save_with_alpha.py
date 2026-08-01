
def test_repeated_save_with_alpha():
    # We want an image which has a background color of bluish green, with an
    # alpha of 0.25.

    fig = Figure([1, 0.4])
    fig.set_facecolor((0, 1, 0.4))
    fig.patch.set_alpha(0.25)

    # The target color is fig.patch.get_facecolor()

    buf = io.BytesIO()

    fig.savefig(buf,
                facecolor=fig.get_facecolor(),
                edgecolor='none')

    # Save the figure again to check that the
    # colors don't bleed from the previous renderer.
    buf.seek(0)
    fig.savefig(buf,
                facecolor=fig.get_facecolor(),
                edgecolor='none')

    # Check the first pixel has the desired color & alpha
    # (approx: 0, 1.0, 0.4, 0.25)
    buf.seek(0)
    assert_array_almost_equal(tuple(imread(buf)[0, 0]),
                              (0.0, 1.0, 0.4, 0.250),
                              decimal=3)

