
def test_mixed_collection():
    # First illustrate basic pyplot interface, using defaults where possible.
    fig, ax = plt.subplots()

    c = mpatches.Circle((8, 8), radius=4, facecolor='none', edgecolor='green')

    # PDF can optimize this one
    p1 = mpl.collections.PatchCollection([c], match_original=True)
    p1.set_offsets([[0, 0], [24, 24]])
    p1.set_linewidths([1, 5])

    # PDF can't optimize this one, because the alpha of the edge changes
    p2 = mpl.collections.PatchCollection([c], match_original=True)
    p2.set_offsets([[48, 0], [-32, -16]])
    p2.set_linewidths([1, 5])
    p2.set_edgecolors([[0, 0, 0.1, 1.0], [0, 0, 0.1, 0.5]])

    ax.patch.set_color('0.5')
    ax.add_collection(p1)
    ax.add_collection(p2)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)

