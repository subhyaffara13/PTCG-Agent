
def test_savefig_tight():
    # Check that the draw-disabled renderer correctly disables open/close_group
    # as well.
    plt.savefig(BytesIO(), format="svgz", bbox_inches="tight")

