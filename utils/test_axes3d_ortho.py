
def test_axes3d_ortho():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_proj_type('ortho')

