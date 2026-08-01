
def test_zordered_error():
    # Smoke test for https://github.com/matplotlib/matplotlib/issues/26497
    lc = [(np.fromiter([0.0, 0.0, 0.0], dtype="float"),
           np.fromiter([1.0, 1.0, 1.0], dtype="float"))]
    pc = [np.fromiter([0.0, 0.0], dtype="float"),
          np.fromiter([0.0, 1.0], dtype="float"),
          np.fromiter([1.0, 1.0], dtype="float")]

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.add_collection(Line3DCollection(lc), autolim="_datalim_only")
    ax.scatter(*pc, visible=False)
    plt.draw()

