
def test_inset_axes_tight():
    # gh-26287 found that inset_axes raised with bbox_inches=tight
    fig, ax = plt.subplots()
    inset_axes(ax, width=1.3, height=0.9)

    f = io.BytesIO()
    fig.savefig(f, bbox_inches="tight")

