
def test_arc_pathpatch():
    ax = plt.subplot(1, 1, 1, projection="3d")
    a = mpatch.Arc((0.5, 0.5), width=0.5, height=0.9,
                   angle=20, theta1=10, theta2=130)
    ax.add_patch(a)
    art3d.pathpatch_2d_to_3d(a, z=0, zdir='z')

