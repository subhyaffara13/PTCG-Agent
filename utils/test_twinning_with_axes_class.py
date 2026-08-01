
def test_twinning_with_axes_class():
    """Check that twinx/y(axes_class=...) gives the appropriate class."""
    _, ax = plt.subplots()
    twinx = ax.twinx(axes_class=SubclassAxes, foo=1)
    assert isinstance(twinx, SubclassAxes)
    assert twinx.foo == 1
    twiny = ax.twiny(axes_class=SubclassAxes, foo=2)
    assert isinstance(twiny, SubclassAxes)
    assert twiny.foo == 2

