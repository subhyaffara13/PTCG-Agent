
def test_axeswidget_del_on_failed_init():
    """
    Test that an unraisable exception is not created when initialization
    fails.
    """
    # Pytest would fail the test if such an exception occurred.
    fig, ax = plt.subplots()
    with pytest.raises(TypeError, match="unexpected keyword argument 'undefined'"):
        widgets.Button(ax, undefined='bar')

