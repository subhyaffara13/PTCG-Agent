
def test_patch_modification():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    circle = Circle((0, 0))
    ax.add_patch(circle)
    art3d.patch_2d_to_3d(circle)
    circle.set_facecolor((1.0, 0.0, 0.0, 1))

    assert mcolors.same_color(circle.get_facecolor(), (1, 0, 0, 1))
    fig.canvas.draw()
    assert mcolors.same_color(circle.get_facecolor(), (1, 0, 0, 1))

