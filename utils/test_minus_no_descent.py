
def test_minus_no_descent(fontsize):
    # Test special-casing of minus descent in DviFont._height_depth_of, by
    # checking that overdrawing a 1 and a -1 results in an overall height
    # equivalent to drawing either of them separately.
    mpl.style.use("mpl20")
    mpl.rcParams['font.size'] = fontsize
    heights = {}
    fig = plt.figure()
    for vals in [(1,), (-1,), (-1, 1)]:
        fig.clear()
        for x in vals:
            fig.text(.5, .5, f"${x}$", usetex=True)
        fig.canvas.draw()
        # The following counts the number of non-fully-blank pixel rows.
        heights[vals] = ((np.array(fig.canvas.buffer_rgba())[..., 0] != 255)
                         .any(axis=1).sum())
    assert len({*heights.values()}) == 1

