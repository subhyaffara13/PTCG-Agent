
def test_autoscale_tight():
    fig, ax = plt.subplots(1, 1)
    ax.plot([1, 2, 3, 4])
    ax.autoscale(enable=True, axis='x', tight=False)
    ax.autoscale(enable=True, axis='y', tight=True)
    assert_allclose(ax.get_xlim(), (-0.15, 3.15))
    assert_allclose(ax.get_ylim(), (1.0, 4.0))

    # Check that autoscale is on
    assert ax.get_autoscalex_on()
    assert ax.get_autoscaley_on()
    assert ax.get_autoscale_on()
    # Set enable to None
    ax.autoscale(enable=None)
    # Same limits
    assert_allclose(ax.get_xlim(), (-0.15, 3.15))
    assert_allclose(ax.get_ylim(), (1.0, 4.0))
    # autoscale still on
    assert ax.get_autoscalex_on()
    assert ax.get_autoscaley_on()
    assert ax.get_autoscale_on()

