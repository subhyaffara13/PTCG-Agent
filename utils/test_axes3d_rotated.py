
def test_axes3d_rotated():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.view_init(90, 45, 0)  # look down, rotated. Should be square

