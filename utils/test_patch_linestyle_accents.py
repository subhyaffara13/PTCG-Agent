
def test_patch_linestyle_accents():
    #: Test if linestyle can also be specified with short mnemonics like "--"
    #: c.f. GitHub issue #2136
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    # concatenate the star with an internal cutout of the circle
    verts = np.concatenate([circle.vertices, star.vertices[::-1]])
    codes = np.concatenate([circle.codes, star.codes])

    linestyles = ["-", "--", "-.", ":",
                  "solid", "dashed", "dashdot", "dotted"]

    fig, ax = plt.subplots()
    for i, ls in enumerate(linestyles):
        star = mpath.Path(verts + i, codes)
        patch = mpatches.PathPatch(star,
                                   linewidth=3, linestyle=ls,
                                   facecolor=(1, 0, 0),
                                   edgecolor=(0, 0, 1))
        ax.add_patch(patch)

    ax.set_xlim([-1, i + 1])
    ax.set_ylim([-1, i + 1])
    fig.canvas.draw()

