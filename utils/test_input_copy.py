
def test_input_copy(fig_test, fig_ref):

    t = np.arange(0, 6, 2)
    l, = fig_test.add_subplot().plot(t, t, ".-")
    t[:] = range(3)
    # Trigger cache invalidation
    l.set_drawstyle("steps")
    fig_ref.add_subplot().plot([0, 2, 4], [0, 2, 4], ".-", drawstyle="steps")

