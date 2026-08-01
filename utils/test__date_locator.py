
def test_DateLocator():
    locator = mdates.DateLocator()
    # Test nonsingular
    assert locator.nonsingular(0, np.inf) == (0, 1)
    assert locator.nonsingular(0, 1) == (0, 1)
    assert locator.nonsingular(1, 0) == (0, 1)
    assert locator.nonsingular(0, 0) == (-2, 2)
    locator.create_dummy_axis()
    # default values
    assert locator.datalim_to_dt() == (
        datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        datetime.datetime(1970, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))

    # Check default is UTC
    assert locator.tz == mdates.UTC
    tz_str = 'Iceland'
    iceland_tz = dateutil.tz.gettz(tz_str)
    # Check not Iceland
    assert locator.tz != iceland_tz
    # Set it to Iceland
    locator.set_tzinfo('Iceland')
    # Check now it is Iceland
    assert locator.tz == iceland_tz
    locator.create_dummy_axis()
    locator.axis.set_data_interval(*mdates.date2num(["2022-01-10",
                                                     "2022-01-08"]))
    assert locator.datalim_to_dt() == (
        datetime.datetime(2022, 1, 8, 0, 0, tzinfo=iceland_tz),
        datetime.datetime(2022, 1, 10, 0, 0, tzinfo=iceland_tz))

    # Set rcParam
    plt.rcParams['timezone'] = tz_str

    # Create a new one in a similar way
    locator = mdates.DateLocator()
    # Check now it is Iceland
    assert locator.tz == iceland_tz

    # Test invalid tz values
    with pytest.raises(ValueError, match="Aiceland is not a valid timezone"):
        mdates.DateLocator(tz="Aiceland")
    with pytest.raises(TypeError,
                       match="tz must be string or tzinfo subclass."):
        mdates.DateLocator(tz=1)

