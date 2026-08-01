
def test_twin_with_aspect(twin):
    fig, ax = plt.subplots()
    # test twinx or twiny
    ax_twin = getattr(ax, f'twin{twin}')()
    ax.set_aspect(5)
    ax_twin.set_aspect(2)
    assert_array_equal(ax.bbox.extents,
                       ax_twin.bbox.extents)

