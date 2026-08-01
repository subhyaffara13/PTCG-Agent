
def test_axes_clear_reference_cycle():
    def assert_not_in_reference_cycle(start):
        # Breadth first search. Return True if we encounter the starting node
        to_visit = deque([start])
        explored = set()
        while len(to_visit) > 0:
            parent = to_visit.popleft()
            for child in gc.get_referents(parent):
                if id(child) in explored:
                    continue
                assert child is not start
                explored.add(id(child))
                to_visit.append(child)

    fig = Figure()
    ax = fig.add_subplot()
    points = np.random.rand(1000)
    ax.plot(points, points)
    ax.scatter(points, points)
    ax_children = ax.get_children()
    fig.clear()  # This should break the reference cycle

    # Care most about the objects that scale with number of points
    big_artists = [
        a for a in ax_children
        if isinstance(a, (Line2D, PathCollection))
    ]
    assert len(big_artists) > 0
    for big_artist in big_artists:
        assert_not_in_reference_cycle(big_artist)
    assert len(ax_children) > 0
    for child in ax_children:
        # Make sure this doesn't raise because the child is already removed.
        try:
            child.remove()
        except NotImplementedError:
            pass  # not implemented is expected for some artists

