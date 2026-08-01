
def test_collection():
    x, y = np.meshgrid(np.linspace(0, 10, 150), np.linspace(-5, 5, 100))
    data = np.sin(x) + np.cos(y)
    cs = plt.contour(data)
    cs.set(path_effects=[
        path_effects.PathPatchEffect(edgecolor='black', facecolor='none', linewidth=12),
        path_effects.Stroke(linewidth=5)])
    for text in plt.clabel(cs, colors='white'):
        text.set_path_effects([path_effects.withStroke(foreground='k',
                                                       linewidth=3)])
        text.set_bbox({'boxstyle': 'sawtooth', 'facecolor': 'none',
                       'edgecolor': 'blue'})

