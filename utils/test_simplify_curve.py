
def test_simplify_curve():
    pp1 = patches.PathPatch(
        Path([(0, 0), (1, 0), (1, 1), (np.nan, 1), (0, 0), (2, 0), (2, 2),
              (0, 0)],
             [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3,
              Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
        fc="none")

    fig, ax = plt.subplots()
    ax.add_patch(pp1)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)

