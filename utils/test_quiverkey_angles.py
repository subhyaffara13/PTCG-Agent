
def test_quiverkey_angles():
    # Check that only a single arrow is plotted for a quiverkey when an array
    # of angles is given to the original quiver plot
    fig, ax = plt.subplots()

    X, Y = np.meshgrid(np.arange(2), np.arange(2))
    U = V = angles = np.ones_like(X)

    q = ax.quiver(X, Y, U, V, angles=angles)
    qk = ax.quiverkey(q, 1, 1, 2, 'Label')
    # The arrows are only created when the key is drawn
    fig.canvas.draw()
    assert len(qk.vector.get_paths()) == 1

