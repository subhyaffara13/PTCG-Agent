
def test_collapsed():
    # test that if the amount of space required to make all the axes
    # decorations fit would mean that the actual Axes would end up with size
    # zero (i.e. margins add up to more than the available width) that a call
    # to tight_layout will not get applied:
    fig, ax = plt.subplots(tight_layout=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.annotate('BIG LONG STRING', xy=(1.25, 2), xytext=(10.5, 1.75),
                annotation_clip=False)
    p1 = ax.get_position()
    with pytest.warns(UserWarning):
        plt.tight_layout()
        p2 = ax.get_position()
        assert p1.width == p2.width
    # test that passing a rect doesn't crash...
    with pytest.warns(UserWarning):
        plt.tight_layout(rect=[0, 0, 0.8, 0.8])

