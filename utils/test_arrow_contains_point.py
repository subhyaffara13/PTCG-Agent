
def test_arrow_contains_point():
    # fix bug (#8384)
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)

    # create an arrow with Curve style
    arrow = patches.FancyArrowPatch((0.5, 0.25), (1.5, 0.75),
                                    arrowstyle='->',
                                    mutation_scale=40)
    ax.add_patch(arrow)
    # create an arrow with Bracket style
    arrow1 = patches.FancyArrowPatch((0.5, 1), (1.5, 1.25),
                                     arrowstyle=']-[',
                                     mutation_scale=40)
    ax.add_patch(arrow1)
    # create an arrow with other arrow style
    arrow2 = patches.FancyArrowPatch((0.5, 1.5), (1.5, 1.75),
                                     arrowstyle='fancy',
                                     fill=False,
                                     mutation_scale=40)
    ax.add_patch(arrow2)
    patches_list = [arrow, arrow1, arrow2]

    # generate some points
    X, Y = np.meshgrid(np.arange(0, 2, 0.1),
                       np.arange(0, 2, 0.1))
    for k, (x, y) in enumerate(zip(X.ravel(), Y.ravel())):
        xdisp, ydisp = ax.transData.transform([x, y])
        event = MouseEvent('button_press_event', fig.canvas, xdisp, ydisp)
        for m, patch in enumerate(patches_list):
            # set the points to red only if the arrow contains the point
            inside, res = patch.contains(event)
            if inside:
                ax.scatter(x, y, s=5, c="r")

