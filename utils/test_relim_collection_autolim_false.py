
def test_relim_collection_autolim_false():
    # GH#30859 - Collection added with autolim=False must not participate
    # in relim() later.
    import matplotlib.collections as mcollections
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    ax.relim()
    expected = ax.dataLim.frozen()
    # Build a collection far outside current limits and add it with autolim=False.
    sc = mcollections.PathCollection([])
    sc.set_offsets([[100, 200], [300, 400]])
    ax.add_collection(sc, autolim=False)
    ax.relim()
    # dataLim must remain unchanged because autolim=False was requested.
    assert_allclose(ax.dataLim.get_points(), expected.get_points())
    assert_allclose(ax.dataLim.minpos, expected.minpos)

