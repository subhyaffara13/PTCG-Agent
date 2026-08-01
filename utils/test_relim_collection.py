
def test_relim_collection():
    fig, ax = plt.subplots()
    sc = ax.scatter([1, 2, 3], [4, 5, 6])
    ax.relim()
    expected = sc.get_datalim(ax.transData)
    assert_allclose(ax.dataLim.get_points(), expected.get_points())
    assert_allclose(ax.dataLim.minpos, expected.minpos)

    # After updating offsets, relim should track the new data.
    sc.set_offsets([[10, 20], [30, 40]])
    ax.relim()
    expected = sc.get_datalim(ax.transData)
    assert_allclose(ax.dataLim.get_points(), expected.get_points())
    assert_allclose(ax.dataLim.minpos, expected.minpos)

    # visible_only=True should ignore hidden collections.
    line, = ax.plot([0, 1], [0, 1])
    sc.set_visible(False)
    ax.relim(visible_only=True)
    # With scatter hidden, limits should be driven by the line only.
    assert_allclose(ax.dataLim.get_points(), [[0, 0], [1, 1]])
    # minpos is the minimum *positive* value; line data [0, 1] gives 1.0.
    assert_array_equal(ax.dataLim.minpos, [1., 1.])

