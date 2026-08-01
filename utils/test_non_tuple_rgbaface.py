
def test_non_tuple_rgbaface():
    # This passes rgbaFace as an ndarray to draw_path.
    fig = plt.figure()
    fig.add_subplot(projection="3d").scatter(
        [0, 1, 2], [0, 1, 2], path_effects=[patheffects.Stroke(linewidth=4)])
    fig.canvas.draw()

