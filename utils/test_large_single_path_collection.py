
def test_large_single_path_collection():
    buff = io.BytesIO()

    # Generates a too-large single path in a path collection that
    # would cause a segfault if the draw_markers optimization is
    # applied.
    f, ax = plt.subplots()
    collection = collections.PathCollection(
        [Path([[-10, 5], [10, 5], [10, -5], [-10, -5], [-10, 5]])])
    ax.add_artist(collection)
    ax.set_xlim(10**-3, 1)
    plt.savefig(buff)

