
def test_axes3d_cla():
    # fixed in pull request 4553
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_axis_off()
    ax.cla()  # make sure the axis displayed is 3D (not 2D)

