
def test_jpl_datetime_units_consistent():
    import matplotlib.testing.jpl_units as units
    units.register()

    dt = datetime(2009, 4, 26)
    jpl = units.Epoch("ET", dt=dt)
    dt_conv = munits.registry.get_converter(dt).convert(dt, None, None)
    jpl_conv = munits.registry.get_converter(jpl).convert(jpl, None, None)
    assert dt_conv == jpl_conv

