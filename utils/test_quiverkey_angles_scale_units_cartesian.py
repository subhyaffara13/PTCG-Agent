
def test_quiverkey_angles_scale_units_cartesian():
    # GH 26316
    # Test that only one arrow will be plotted with normal cartesian
    # when angles='xy' and/or scale_units='xy'

    kwargs_list = [
        {'angles': 'xy'},
        {'angles': 'xy', 'scale_units': 'xy'},
        {'scale_units': 'xy'}
    ]

    for kwargs_dict in kwargs_list:
        X = [0, -1, 0]
        Y = [0, -1, 0]
        U = [1, -1, 1]
        V = [1, -1, 0]

        fig, ax = plt.subplots()
        q = ax.quiver(X, Y, U, V, **kwargs_dict)
        ax.quiverkey(q, X=0.3, Y=1.1, U=1,
                     label='Quiver key, length = 1', labelpos='E')
        qk = ax.quiverkey(q, 0, 0, 1, '1 units')

        fig.canvas.draw()
        assert len(qk.vector.get_paths()) == 1

