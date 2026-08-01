
def test_hatching():
    fig, ax = plt.subplots(1, 1)

    # Default hatch color.
    rect1 = mpatches.Rectangle((0, 0), 3, 4, hatch='/')
    ax.add_patch(rect1)

    rect2 = mcollections.RegularPolyCollection(
        4, sizes=[16000], offsets=[(1.5, 6.5)], offset_transform=ax.transData,
        hatch='/')
    ax.add_collection(rect2)

    # Ensure edge color is not applied to hatching.
    rect3 = mpatches.Rectangle((4, 0), 3, 4, hatch='/', edgecolor='C1')
    ax.add_patch(rect3)

    rect4 = mcollections.RegularPolyCollection(
        4, sizes=[16000], offsets=[(5.5, 6.5)], offset_transform=ax.transData,
        hatch='/', edgecolor='C1')
    ax.add_collection(rect4)

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 9)


def test_hatching():
    # Remove legend texts when this image is regenerated.
    fig, ax = plt.subplots()

    # Patches
    patch = plt.Rectangle((0, 0), 0.3, 0.3, hatch='xx',
                          label='Patch\ndefault color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0), 0.3, 0.3, hatch='||', edgecolor='C1',
                          label='Patch\nexplicit color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0, 0.4), 0.3, 0.3, hatch='xx', fill=False,
                          label='Patch\ndefault color\nunfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0.4), 0.3, 0.3, hatch='||', fill=False,
                          edgecolor='C1',
                          label='Patch\nexplicit color\nunfilled')
    ax.add_patch(patch)

    # Paths
    ax.fill_between([0, .15, .3], [.8, .8, .8], [.9, 1.0, .9],
                    hatch='+', label='Path\ndefault color')
    ax.fill_between([.33, .48, .63], [.8, .8, .8], [.9, 1.0, .9],
                    hatch='+', edgecolor='C2', label='Path\nexplicit color')

    ax.set_xlim(-0.01, 1.1)
    ax.set_ylim(-0.01, 1.1)
    ax.legend(handlelength=4, handleheight=4)

