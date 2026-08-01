
def test_limits_after_scroll_zoom():
    fig, ax = plt.subplots()
    #
    xlim = (-0.5, 0.5)
    ylim = (-1, 2)
    ax.set_xlim(xlim)
    ax.set_ylim(ymin=ylim[0], ymax=ylim[1])
    # This is what scroll zoom calls:
    # Zoom with factor 1, small numerical change
    ax._set_view_from_bbox((200, 200, 1.))
    np.testing.assert_allclose(xlim, ax.get_xlim(), atol=1e-16)
    np.testing.assert_allclose(ylim, ax.get_ylim(), atol=1e-16)

    # Zoom in
    ax._set_view_from_bbox((200, 200, 2.))
    # Hard-coded values
    new_xlim = (-0.3790322580645161, 0.12096774193548387)
    new_ylim = (-0.40625, 1.09375)

    res_xlim = ax.get_xlim()
    res_ylim = ax.get_ylim()
    np.testing.assert_allclose(res_xlim[1] - res_xlim[0], 0.5)
    np.testing.assert_allclose(res_ylim[1] - res_ylim[0], 1.5)
    np.testing.assert_allclose(new_xlim, res_xlim, atol=1e-16)
    np.testing.assert_allclose(new_ylim, res_ylim)

    # Zoom out, should be same as before, except for numerical issues
    ax._set_view_from_bbox((200, 200, 0.5))
    res_xlim = ax.get_xlim()
    res_ylim = ax.get_ylim()
    np.testing.assert_allclose(res_xlim[1] - res_xlim[0], 1)
    np.testing.assert_allclose(res_ylim[1] - res_ylim[0], 3)
    np.testing.assert_allclose(xlim, res_xlim, atol=1e-16)
    np.testing.assert_allclose(ylim, res_ylim, atol=1e-16)

