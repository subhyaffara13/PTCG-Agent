
def test_unsupported_td64_unit_raises(unit):
    # GH 52806
    with pytest.raises(
        ValueError,
        match=f"Unit {unit} is not supported. "
        "Only unambiguous timedelta values durations are supported. "
        "Allowed units are 'W', 'D', 'h', 'm', 's', 'ms', 'us', 'ns'",
    ):
        Timedelta(np.timedelta64(1, unit))

