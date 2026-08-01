
def test_DayLocator():
    with pytest.raises(ValueError):
        mdates.DayLocator(interval=-1)
    with pytest.raises(ValueError):
        mdates.DayLocator(interval=-1.5)
    with pytest.raises(ValueError):
        mdates.DayLocator(interval=0)
    with pytest.raises(ValueError):
        mdates.DayLocator(interval=1.3)
    mdates.DayLocator(interval=1.0)

