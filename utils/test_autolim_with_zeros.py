
def test_autolim_with_zeros(transform, expected):
    # 1) Test that a scatter at (0, 0) data coordinates contributes to
    # autoscaling even though any(offsets) would be False in that situation.
    # 2) Test that specifying transAxes for the transform does not contribute
    # to the autoscaling.
    fig, ax = plt.subplots()
    ax.scatter(0, 0, transform=getattr(ax, transform))
    ax.scatter(3, 3)
    np.testing.assert_allclose(ax.get_ylim(), expected)
    np.testing.assert_allclose(ax.get_xlim(), expected)

