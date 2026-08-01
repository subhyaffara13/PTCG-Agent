
def test_maxlength_no_broken():
    x, y, U, V = swirl_velocity_field()
    ax = plt.figure().subplots()
    ax.streamplot(x, y, U, V, maxlength=10., start_points=[[0., 1.5]],
                  linewidth=2, density=2, broken_streamlines=False)
    assert ax.get_xlim()[-1] == ax.get_ylim()[-1] == 3
    # Compatibility for old test image
    ax.set(xlim=(None, 3.2555988021882305), ylim=(None, 3.078326760195413))

