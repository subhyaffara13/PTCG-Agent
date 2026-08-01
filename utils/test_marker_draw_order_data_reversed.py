
def test_marker_draw_order_data_reversed(fig_test, fig_ref, azim):
    """
    Test that the draw order does not depend on the data point order.

    For the given viewing angle at azim=-50, the yellow marker should be in
    front. For azim=130, the blue marker should be in front.
    """
    x = [-1, 1]
    y = [1, -1]
    z = [0, 0]
    color = ['b', 'y']
    ax = fig_test.add_subplot(projection='3d')
    ax.scatter(x, y, z, s=3500, c=color)
    ax.view_init(elev=0, azim=azim, roll=0)
    ax = fig_ref.add_subplot(projection='3d')
    ax.scatter(x[::-1], y[::-1], z[::-1], s=3500, c=color[::-1])
    ax.view_init(elev=0, azim=azim, roll=0)

