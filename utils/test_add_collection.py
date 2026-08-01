
def test_add_collection():
    # Test if data limits are unchanged by adding an empty collection.
    # GitHub issue #1490, pull #1497.
    plt.figure()
    ax = plt.axes()
    ax.scatter([0, 1], [0, 1])
    bounds = ax.dataLim.bounds
    ax.scatter([], [])
    assert ax.dataLim.bounds == bounds

