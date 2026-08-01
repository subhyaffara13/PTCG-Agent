
def test_indicate_inset_inverted(x_inverted, y_inverted):
    """
    Test that the inset lines are correctly located with inverted data axes.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2)

    x = np.arange(10)
    ax1.plot(x, x, 'o')
    if x_inverted:
        ax1.invert_xaxis()
    if y_inverted:
        ax1.invert_yaxis()

    inset = ax1.indicate_inset([2, 2, 5, 4], ax2)
    lower_left, upper_left, lower_right, upper_right = inset.connectors

    sign_x = -1 if x_inverted else 1
    sign_y = -1 if y_inverted else 1
    assert sign_x * (lower_right.xy2[0] - lower_left.xy2[0]) > 0
    assert sign_x * (upper_right.xy2[0] - upper_left.xy2[0]) > 0
    assert sign_y * (upper_left.xy2[1] - lower_left.xy2[1]) > 0
    assert sign_y * (upper_right.xy2[1] - lower_right.xy2[1]) > 0

