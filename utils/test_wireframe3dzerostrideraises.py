
def test_wireframe3dzerostrideraises():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    with pytest.raises(ValueError):
        ax.plot_wireframe(X, Y, Z, rstride=0, cstride=0)

