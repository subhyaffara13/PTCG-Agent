
def test_tick_normalize_raises(tick_classes):
    # check that trying to create a Tick object with normalize=True raises
    # GH#21427
    cls = tick_classes
    msg = "Tick offset with `normalize=True` are not allowed."
    with pytest.raises(ValueError, match=msg):
        cls(n=3, normalize=True)

