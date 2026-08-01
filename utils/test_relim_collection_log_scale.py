
def test_relim_collection_log_scale():
    # GH#30859 - relim() for Collection on a log-scaled axis should
    # correctly propagate minpos into dataLim.
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.set_yscale('log')
    sc = ax.scatter([1e-3, 1e-2, 1e-1], [1e1, 1e2, 1e3])
    sc.set_offsets([[1e1, 1e4], [1e2, 1e5]])
    ax.relim()
    expected = sc.get_datalim(ax.transData)
    assert_allclose(ax.dataLim.get_points(), expected.get_points())
    assert_allclose(ax.dataLim.minpos, expected.minpos)

