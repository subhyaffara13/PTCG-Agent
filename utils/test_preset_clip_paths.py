
def test_preset_clip_paths():
    fig, ax = plt.subplots()

    poly = mpl.patches.Polygon(
        [[1, 0], [0, 1], [-1, 0], [0, -1]], facecolor="#ddffdd",
        edgecolor="#00ff00", linewidth=2, alpha=0.5)

    ax.add_patch(poly)

    line = mpl.lines.Line2D((-1, 1), (0.5, 0.5), clip_on=True, clip_path=poly)
    line.set_path_effects([patheffects.withTickedStroke()])
    ax.add_artist(line)

    line = mpl.lines.Line2D((-1, 1), (-0.5, -0.5), color='r', clip_on=True,
                            clip_path=poly)
    ax.add_artist(line)

    poly2 = mpl.patches.Polygon(
        [[-1, 1], [0, 1], [0, -0.25]], facecolor="#beefc0", alpha=0.3,
        edgecolor="#faded0", linewidth=2, clip_on=True, clip_path=poly)
    ax.add_artist(poly2)

    # When text clipping works, the "Annotation" text should be clipped
    ax.annotate('Annotation', (-0.75, -0.75), xytext=(0.1, 0.75),
                arrowprops={'color': 'k'}, clip_on=True, clip_path=poly)

    poly3 = mpl.patches.Polygon(
        [[0, 0], [0, 0.5], [0.5, 0.5], [0.5, 0]], facecolor="g", edgecolor="y",
        linewidth=2, alpha=0.3, clip_on=True, clip_path=poly)

    fig.add_artist(poly3, clip=True)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

