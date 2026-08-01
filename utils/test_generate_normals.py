
def test_generate_normals():
    # Smoke test for https://github.com/matplotlib/matplotlib/issues/29156
    vertices = ((0, 0, 0), (0, 5, 0), (5, 5, 0), (5, 0, 0))
    shape = Poly3DCollection([vertices], edgecolors='r', shade=True)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.add_collection3d(shape)
    plt.draw()

