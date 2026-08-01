
def test_stairs_update(fig_test, fig_ref):
    # fixed ylim because stairs() does autoscale, but updating data does not
    ylim = -3, 4
    # Test
    test_ax = fig_test.add_subplot()
    h = test_ax.stairs([1, 2, 3])
    test_ax.set_ylim(ylim)
    h.set_data([3, 2, 1])
    h.set_data(edges=np.arange(4)+2)
    h.set_data([1, 2, 1], np.arange(4)/2)
    h.set_data([1, 2, 3])
    h.set_data(None, np.arange(4))
    assert np.allclose(h.get_data()[0], np.arange(1, 4))
    assert np.allclose(h.get_data()[1], np.arange(4))
    h.set_data(baseline=-2)
    assert h.get_data().baseline == -2

    # Ref
    ref_ax = fig_ref.add_subplot()
    h = ref_ax.stairs([1, 2, 3], baseline=-2)
    ref_ax.set_ylim(ylim)

