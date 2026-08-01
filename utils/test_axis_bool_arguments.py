
def test_axis_bool_arguments(fig_test, fig_ref):
    # Test if False and "off" give the same
    fig_test.add_subplot(211).axis(False)
    fig_ref.add_subplot(211).axis("off")
    # Test if True after False gives the same as "on"
    ax = fig_test.add_subplot(212)
    ax.axis(False)
    ax.axis(True)
    fig_ref.add_subplot(212).axis("on")

