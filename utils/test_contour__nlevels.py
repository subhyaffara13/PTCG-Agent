
def test_contour_Nlevels():
    # A scalar levels arg or kwarg should trigger auto level generation.
    # https://github.com/matplotlib/matplotlib/issues/11913
    z = np.arange(12).reshape((3, 4))
    fig, ax = plt.subplots()
    cs1 = ax.contour(z, 5)
    assert len(cs1.levels) > 1
    cs2 = ax.contour(z, levels=5)
    assert (cs1.levels == cs2.levels).all()

