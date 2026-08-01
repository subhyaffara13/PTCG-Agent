
def test_PathEffect_points_to_pixels():
    fig = plt.figure(dpi=150)
    p1, = plt.plot(range(10))
    p1.set_path_effects([path_effects.SimpleLineShadow(),
                         path_effects.Normal()])
    renderer = fig.canvas.get_renderer()
    pe_renderer = path_effects.PathEffectRenderer(
        p1.get_path_effects(), renderer)
    # Confirm that using a path effects renderer maintains point sizes
    # appropriately. Otherwise rendered font would be the wrong size.
    assert renderer.points_to_pixels(15) == pe_renderer.points_to_pixels(15)

