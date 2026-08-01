
def test_quiverkey_angles_xy_aitoff():
    # GH 26316 and GH 26748
    # Test that only one arrow will be plotted with non-cartesian
    # when angles='xy' and/or scale_units='xy'

    # only for test purpose
    # scale_units='xy' may not be a valid use case for non-cartesian
    kwargs_list = [
        {'angles': 'xy'},
        {'angles': 'xy', 'scale_units': 'xy'},
        {'scale_units': 'xy'}
    ]

    for kwargs_dict in kwargs_list:

        x = np.linspace(-np.pi, np.pi, 11)
        y = np.ones_like(x) * np.pi / 6
        vx = np.zeros_like(x)
        vy = np.ones_like(x)

        fig = plt.figure()
        ax = fig.add_subplot(projection='aitoff')
        q = ax.quiver(x, y, vx, vy, **kwargs_dict)
        qk = ax.quiverkey(q, 0, 0, 1, '1 units')

        fig.canvas.draw()
        assert len(qk.vector.get_paths()) == 1

