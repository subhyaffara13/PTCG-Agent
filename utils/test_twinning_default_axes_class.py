
def test_twinning_default_axes_class():
    """
    Check that the default class for twinx/y() is Axes,
    even if the original is an Axes subclass.
    """
    _, ax = plt.subplots(subplot_kw=dict(axes_class=SubclassAxes, foo=1))
    twinx = ax.twinx()
    assert type(twinx) is Axes
    twiny = ax.twiny()
    assert type(twiny) is Axes

