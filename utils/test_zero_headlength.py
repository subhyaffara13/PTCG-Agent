
def test_zero_headlength():
    # Based on report by Doug McNeil:
    # https://discourse.matplotlib.org/t/quiver-warnings/16722
    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.arange(10), np.arange(10))
    U, V = np.cos(X), np.sin(Y)
    ax.quiver(U, V, headlength=0, headaxislength=0)
    fig.canvas.draw()  # Check that no warning is emitted.

