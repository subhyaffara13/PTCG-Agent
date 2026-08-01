
def test_set_ticks_kwargs_raise_error_without_labels():
    """
    When labels=None and any kwarg is passed, axis.set_ticks() raises a
    ValueError.
    """
    fig, ax = plt.subplots()
    ticks = [1, 2, 3]
    with pytest.raises(ValueError, match="Incorrect use of keyword argument 'alpha'"):
        ax.xaxis.set_ticks(ticks, alpha=0.5)

